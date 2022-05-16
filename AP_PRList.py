import json, requests

r = requests.get("https://api.github.com/search/issues?q=is:pr%20label:DevCallTopic%20repo:ardupilot/ardupilot")
j = json.loads(r.content)

for pr in j["items"]:
    print(pr["html_url"])
