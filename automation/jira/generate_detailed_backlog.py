import json

with open("automation/jira/backlog.json") as f:
    data = json.load(f)

templates = {
1:["Validate DEV environment","Configure repository standards","Validate Docker baseline","Document DEV architecture"],
2:["Build REST API ingestion","Build file ingestion","Build PostgreSQL ingestion","Implement failure handling"],
3:["Build Raw zone","Build Clean zone","Build Curated zone","Implement data quality controls"],
4:["Configure PySpark","Build transformations","Implement incremental processing","Test Spark pipeline"],
5:["Configure BigQuery","Build warehouse model","Load curated data","Validate warehouse"],
6:["Configure dbt","Build models","Implement dbt tests","Generate lineage documentation"],
7:["Deploy Airflow","Build DAGs","Implement retries and alerts","Validate orchestration"],
8:["Design product hierarchy","Generate Product Master","Implement lifecycle model","Validate product data"],
9:["Build semantic model","Build operational dashboards","Build Executive Cockpit","Validate Power BI"],
10:["Prepare ML datasets","Build forecasting models","Build anomaly detection","Validate models"],
11:["Deploy PROD","Implement security controls","Implement monitoring","Validate PROD"],
12:["Implement backup strategy","Test restore and DR","Document migration","Finalize portfolio"]
}

out=[]

for epic in data["epics"]:
    tasks=templates[epic["week"]]
    hours=epic["hours"]
    base=hours//len(tasks)
    remainder=hours%len(tasks)

    children=[]
    for i,title in enumerate(tasks):
        estimate=base+(1 if i < remainder else 0)
        children.append({
            "type":"Story",
            "summary":title,
            "estimate_hours":estimate,
            "priority":epic["priority"]
        })

    out.append({**epic,"stories":children})

with open("automation/jira/backlog_detailed.json","w") as f:
    json.dump({"project":"SCRUM","epics":out},f,indent=2)

print("\n=== DETAILED BACKLOG DRY-RUN ===")
count=0
hours=0

for e in out:
    print(f'\nEPIC-{e["week"]:02} {e["name"]}')
    for s in e["stories"]:
        count+=1
        hours+=s["estimate_hours"]
        print(f'  STORY | {s["summary"]} | {s["estimate_hours"]}h')

print(f"\nEpics: {len(out)}")
print(f"Stories: {count}")
print(f"Hours: {hours}")
print("Jira changes: 0")
print("DRY-RUN: OK")
