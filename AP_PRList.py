from curses import pair_content
import json, requests

pr_search = json.loads(requests.get("https://api.github.com/search/issues?q=is:pr%20label:DevCallTopic%20org:ArduPilot").content)
issue_search = json.loads(requests.get("https://api.github.com/search/issues?q=is:issue%20label:DevCallTopic%20org:ArduPilot").content)

print("**Pull Requests:**\n")
for pr in pr_search["items"]:
    print(pr["html_url"])

print("\n")

print("**Issues:**\n")
for issue in issue_search["items"]:
    print(issue["html_url"])
