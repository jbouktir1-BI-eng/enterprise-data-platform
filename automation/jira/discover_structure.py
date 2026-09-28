import os, json, base64, urllib.request, urllib.parse, urllib.error

BASE=os.environ["JIRA_URL"].rstrip("/")
AUTH=base64.b64encode(
    f'{os.environ["JIRA_EMAIL"]}:{os.environ["JIRA_API_TOKEN"]}'.encode()
).decode()

H={"Authorization":f"Basic {AUTH}","Accept":"application/json"}

def get(path):
    try:
        req=urllib.request.Request(BASE+path,headers=H)
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"ERROR":e.code,"BODY":e.read().decode()}

print("\n=== ISSUE TYPES ===")
types=get("/rest/api/3/issuetype/project?projectId=10000")
for x in types if isinstance(types,list) else []:
    print(f'{x["name"]:15} ID={x["id"]} LEVEL={x.get("hierarchyLevel")} SUBTASK={x.get("subtask")}')

print("\n=== IMPORTANT FIELDS ===")
fields=get("/rest/api/3/field")
wanted=["sprint","story point","start date","due date","time tracking",
        "labels","parent","assignee","priority","status"]
for f in fields if isinstance(fields,list) else []:
    if any(x in f["name"].lower() for x in wanted):
        print(f'{f["name"]:30} -> {f["id"]}')

print("\n=== STATUSES ===")
statuses=get("/rest/api/3/status")
for s in statuses if isinstance(statuses,list) else []:
    print(f'{s["name"]:20} ID={s["id"]}')

print("\n=== BOARDS ===")
boards=get("/rest/agile/1.0/board?projectKeyOrId=SCRUM")
print(json.dumps(boards,indent=2))

if boards.get("values"):
    bid=boards["values"][0]["id"]
    print(f"\n=== SPRINTS BOARD {bid} ===")
    print(json.dumps(get(f"/rest/agile/1.0/board/{bid}/sprint"),indent=2))

print("\n=== TP0 ===")
jql=urllib.parse.quote('project=SCRUM AND summary ~ "W01" ORDER BY key')
print(json.dumps(
    get(f"/rest/api/3/search/jql?jql={jql}&maxResults=20&fields=summary,issuetype,status,priority,assignee,parent,timetracking,labels,duedate"),
    indent=2
))

print("\nDISCOVERY: OK")
