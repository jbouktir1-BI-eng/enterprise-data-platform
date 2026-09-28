import os,json,base64,urllib.request,urllib.parse,urllib.error

BASE=os.environ["JIRA_URL"].rstrip("/")
AUTH=base64.b64encode(
    f'{os.environ["JIRA_EMAIL"]}:{os.environ["JIRA_API_TOKEN"]}'.encode()
).decode()

H={
 "Authorization":f"Basic {AUTH}",
 "Accept":"application/json",
 "Content-Type":"application/json"
}

def call(path,method="GET",data=None):
    req=urllib.request.Request(
        BASE+path,
        data=json.dumps(data).encode() if data is not None else None,
        headers=H,method=method
    )
    try:
        with urllib.request.urlopen(req) as r:
            b=r.read()
            return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        print("ERROR",e.code,path,e.read().decode())
        raise

# ---------------------------------------------------------
# TP0 actual work = 3h32 = 212 min
# Pause 15 min already excluded
# ---------------------------------------------------------

TP0={
 "Validate DEV environment":{
    "estimate":"1h",
    "spent":"55m",
    "points":2,
    "labels":["tp0","dev-environment","completed"]
 },
 "Configure repository standards":{
    "estimate":"1h",
    "spent":"42m",
    "points":2,
    "labels":["tp0","git","github","repository","completed"]
 },
 "Validate Docker baseline":{
    "estimate":"1h",
    "spent":"35m",
    "points":2,
    "labels":["tp0","docker","infrastructure","completed"]
 },
 "Document DEV architecture":{
    "estimate":"1h",
    "spent":"1h",
    "points":3,
    "labels":["tp0","jira","automation","architecture","completed"]
 }
}

# 55 + 42 + 35 + 60 = 192 min
# Remaining 20 min = Jira/API setup recorded on Epic
EPIC_SPENT="20m"

me=call("/rest/api/3/myself")
account=me["accountId"]

jql=urllib.parse.quote('project=SCRUM ORDER BY key')
result=call(
 f"/rest/api/3/search/jql?jql={jql}&maxResults=100"
 "&fields=summary,issuetype,status,parent,worklog"
)

issues=result.get("issues",[])

def done(key):
    ts=call(f"/rest/api/3/issue/{key}/transitions")
    d=next((x for x in ts.get("transitions",[])
            if x["name"].lower()=="done"),None)
    if d:
        call(f"/rest/api/3/issue/{key}/transitions","POST",
             {"transition":{"id":d["id"]}})

def log_work(key,time):
    # Avoid duplicate TP0 worklog
    existing=call(f"/rest/api/3/issue/{key}/worklog")
    for w in existing.get("worklogs",[]):
        comment=w.get("comment",{})
        txt=str(comment)
        if "TP0 automated worklog" in txt:
            print("WORKLOG EXISTS",key)
            return

    call(f"/rest/api/3/issue/{key}/worklog","POST",{
      "timeSpent":time,
      "started":"2026-09-28T14:00:00.000+0000",
      "comment":{
        "type":"doc",
        "version":1,
        "content":[{
          "type":"paragraph",
          "content":[{
            "type":"text",
            "text":"TP0 automated worklog - actual execution time; 15 min break excluded."
          }]
        }]
      }
    })

# ---------------------------------------------------------
# Epic W01
# ---------------------------------------------------------

epic=next(
 (i for i in issues if i["fields"]["summary"]=="W01 - Environment & DEV"),
 None
)

if not epic:
    raise SystemExit("W01 EPIC NOT FOUND")

ekey=epic["key"]

call(f"/rest/api/3/issue/{ekey}","PUT",{
 "fields":{
   "assignee":{"accountId":account},
   "labels":["week-01","tp0","environment","dev","completed"],
   "customfield_10015":"2026-09-28",
   "duedate":"2026-09-28",
   "customfield_10020":2,
   "priority":{"name":"Highest"}
 }
})

log_work(ekey,EPIC_SPENT)
done(ekey)

print("EPIC UPDATED",ekey)

# ---------------------------------------------------------
# TP0 Features
# ---------------------------------------------------------

for summary,cfg in TP0.items():

    issue=next(
      (i for i in issues if i["fields"]["summary"]==summary),
      None
    )

    if not issue:
        print("NOT FOUND",summary)
        continue

    key=issue["key"]

    call(f"/rest/api/3/issue/{key}","PUT",{
      "fields":{
        "assignee":{"accountId":account},
        "labels":cfg["labels"],
        "customfield_10015":"2026-09-28",
        "duedate":"2026-09-28",
        "customfield_10020":2,
        "customfield_10016":cfg["points"],
        "priority":{"name":"Highest"},
        "timetracking":{
          "originalEstimate":cfg["estimate"]
        }
      }
    })

    log_work(key,cfg["spent"])
    done(key)

    print("FEATURE UPDATED",key,summary,cfg["spent"])

print()
print("TP0 ACTUAL TIME = 3h32")
print("BREAK EXCLUDED    = 15m")
print("SPRINT            = SCRUM Sprint 0")
print("STATUS            = Done")
print("FINALIZE TP0: OK")
