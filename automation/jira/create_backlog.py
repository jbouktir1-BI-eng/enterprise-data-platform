import os,json,base64,urllib.request,urllib.error

BASE=os.environ["JIRA_URL"].rstrip("/")
AUTH=base64.b64encode(
    f'{os.environ["JIRA_EMAIL"]}:{os.environ["JIRA_API_TOKEN"]}'.encode()
).decode()

HEADERS={
    "Authorization":f"Basic {AUTH}",
    "Accept":"application/json",
    "Content-Type":"application/json"
}

with open("automation/jira/backlog_detailed.json") as f:
    data=json.load(f)

def create(fields):
    req=urllib.request.Request(
        BASE+"/rest/api/3/issue",
        data=json.dumps({"fields":fields}).encode(),
        headers=HEADERS,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)["key"]
    except urllib.error.HTTPError as e:
        print("ERROR",e.code,e.read().decode())
        raise

created=[]

for epic in data["epics"]:

    epic_key=create({
        "project":{"key":"SCRUM"},
        "issuetype":{"id":"10001"},
        "summary":f'W{epic["week"]:02} - {epic["name"]}'
    })

    print("EPIC",epic_key)
    created.append(epic_key)

    for story in epic["stories"]:
        feature_key=create({
            "project":{"key":"SCRUM"},
            "issuetype":{"id":"10003"},
            "summary":story["summary"],
            "parent":{"key":epic_key},
            "timetracking":{
                "originalEstimate":f'{story["estimate_hours"]}h'
            }
        })

        print("  FEATURE",feature_key)
        created.append(feature_key)

print("\nCREATED:",len(created))
print("JIRA CREATE: OK")
