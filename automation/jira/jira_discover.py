import os
import json
import base64
import urllib.request

BASE = os.environ["JIRA_URL"].rstrip("/")
AUTH = base64.b64encode(
    f'{os.environ["JIRA_EMAIL"]}:{os.environ["JIRA_API_TOKEN"]}'.encode()
).decode()

HEADERS = {
    "Authorization": f"Basic {AUTH}",
    "Accept": "application/json"
}

def get(path):
    req = urllib.request.Request(BASE + path, headers=HEADERS)
    with urllib.request.urlopen(req) as response:
        body = response.read().decode()
        return json.loads(body)

print("=== JIRA CONNECTION ===")
me = get("/rest/api/3/myself")
print("User:", me["displayName"])
print("Active:", me["active"])

print("\n=== PROJECTS ===")
projects = get("/rest/api/3/project")

for project in projects:
    print(
        f'ID={project["id"]} | '
        f'KEY={project["key"]} | '
        f'NAME={project["name"]}'
    )

print("\nDISCOVERY: OK")
