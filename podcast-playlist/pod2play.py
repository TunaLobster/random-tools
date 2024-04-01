from collections import defaultdict
from dataclasses import dataclass
import datetime
from itertools import cycle, islice
import json
import os

from feedgen.feed import FeedGenerator
import feedparser
import listparser
import yaml
import dateutil

try:
    from yaml import CLoader as yaml_loader
except ImportError:
    from yaml import Loader as yaml_loader


# TODO: Move RSS URLs to the yaml and dump the opml stuff. Leverage yaml refence stuff to have feeds: feed: &UpFirst where *UpFirst: name: Up Frist, url: blah

@dataclass
class episode:
    title: str
    url: str
    feed: str
    tier: int
    time_published: datetime.datetime


def roundrobin(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


# load subscribed feeds from opml
result = listparser.parse(open(os.path.join(os.path.dirname(__file__),"opml.xml")).read())
# print("opml =",json.dumps(result,indent=2))
feeds = result["feeds"]
# print("feeds =",feeds)

config = yaml.load(open(os.path.join(os.path.dirname(__file__),"config.yaml")), Loader=yaml_loader)

# fetch each feed
episodes = defaultdict(list)
for feed in feeds:
    fetched = feedparser.parse(feed["url"])
    # print(json.dumps(fetched,indent=2))
    for entry in fetched["entries"]:
        parsed_time = dateutil.parser.parse(entry["published"])
        media_links = tuple(
            x for x in entry["links"] if any(y in x["type"] for y in ("audio", "video"))
        )
        # print(media_links)
        if len(media_links) == 0:
            continue
        episodes[feed["title"]].append(
            episode(
                entry["title"],
                media_links[0]["href"],
                feed["title"],
                tier=1,  # change this to be grabbing the tier from the config
                time_published=parsed_time,
            )
        )
# print(episodes)

# build up list of episodes
# sort order is tier then roundrobin
# print(config)

# create feed from list of episodes
for playlist in config["playlists"]:
    # fg = FeedGenerator()
    # fg.load_extension('podcast')
    # fg.title(playlist["name"])
    # fg.link(href="http://www.google.com")
    # fg.description("Personal ordered collection of podcast feeds")
    # fg.podcast.itunes_category("Technology")

    tiers = defaultdict(list)
    for feed in playlist["feeds"]:
        # print(feed["name"])
        # find the matching feed in the episodes dict
        # slice for the count
        feed_episodes = episodes[feed["name"]][: feed["count"]]
        # sort as per config
        if feed["sort"] == "newest":
            feed_episodes = sorted(feed_episodes, key=lambda x: x.time_published)
        elif feed["sort"] == "oldest":
            feed_episodes = sorted(
                feed_episodes, key=lambda x: x.time_published, reverse=True
            )
        tiers[feed["tier"]].append(feed_episodes)

    ordered = []
    # Round robin build up each tier from individual feeds
    for tier in sorted(tiers.keys()):
        ordered.extend(roundrobin(*tiers[tier]))
    # for item in reversed(ordered):
    #     fe = fg.add_entry()
    #     fe.id(item.url)
    #     fe.link(href=item.url)
    #     fe.description(item.title)
    #     fe.title(f"{item.feed}: {item.title}")
    #     fe.enclosure(item.url,0,"audio/mpeg")

    # Save the playlist to a file
    # fg.rss_str(pretty=True)
    # fg.rss_file(f"{playlist['name']}_rss.xml")

    with open(f"{playlist['name']}_rss.m3u","w") as f:
        f.write("#EXTM3U\n")
        for x in ordered:
            f.write(f"#EXTINF:1,{x.feed}: {x.title.replace(',','').replace('-','')}\n{x.url}\n")
