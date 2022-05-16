import json
import requests
from operator import itemgetter

pr_search = json.loads(requests.get("https://api.github.com/search/issues?q=is:pr%20label:DevCallTopic%20org:ArduPilot").content)
issue_search = json.loads(requests.get("https://api.github.com/search/issues?q=is:issue%20label:DevCallTopic%20org:ArduPilot").content)

# sort the PRs oldest to newest based on PR number
pr_sorted = sorted(pr_search["items"], key=itemgetter("number"))

print("**Pull Requests:**\n")
for pr in pr_sorted:
    print(pr["html_url"])

print("\n")

print("**Issues:**\n")
for issue in issue_search["items"]:
    print(issue["html_url"])
