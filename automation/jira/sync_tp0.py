import os,json,base64,urllib.request,urllib.error

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
        data=json.dumps(data).encode() if data else None,
        headers=H,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as r:
            body=r.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        print("ERROR",path,e.code,e.read().decode())
        raise

# Current user
me=call("/rest/api/3/myself")
account=me["accountId"]

# Delete old sample tickets
for key in ["SCRUM-3","SCRUM-4"]:
    try:
        call(f"/rest/api/3/issue/{key}","DELETE")
        print("DELETED",key)
    except:
        print("SKIP",key)

# Get all project issues
result=call(
    "/rest/api/3/search/jql"
    "?jql=project%3DSCRUM%20ORDER%20BY%20key"
    "&maxResults=100"
    "&fields=summary,priority,status"
)

issues=result.get("issues",[])

for issue in issues:
    key=issue["key"]
    summary=issue["fields"]["summary"]

    priority="High"
    if summary.startswith(("W01","W02","W11","W12")):
        priority="Highest"

    call(f"/rest/api/3/issue/{key}","PUT",{
        "fields":{
            "assignee":{"accountId":account},
            "priority":{"name":priority}
        }
    })

    print("UPDATED",key,priority)

# Mark Week 1 Epic + Features DONE
week1=[
    i for i in issues
    if i["fields"]["summary"].startswith("W01")
    or i["fields"]["summary"] in [
        "Validate DEV environment",
        "Configure repository standards",
        "Validate Docker baseline",
        "Document DEV architecture"
    ]
]

for issue in week1:
    key=issue["key"]
    transitions=call(f"/rest/api/3/issue/{key}/transitions")

    done=next(
        (t for t in transitions.get("transitions",[])
         if t["name"].lower() in ["done","complete","completed"]),
        None
    )

    if done:
        call(
            f"/rest/api/3/issue/{key}/transitions",
            "POST",
            {"transition":{"id":done["id"]}}
        )
        print("DONE",key)
    else:
        print("NO DONE TRANSITION",key)

print("\nTP0 SYNC: OK")
