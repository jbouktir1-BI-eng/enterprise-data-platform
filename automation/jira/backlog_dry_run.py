import json

with open("automation/jira/backlog.json") as f:
    data = json.load(f)

print("\n=== JIRA BACKLOG DRY-RUN ===\n")

total = 0

for epic in data["epics"]:
    total += epic["hours"]
    print(
        f'EPIC-{epic["week"]:02} | '
        f'{epic["name"]:<35} | '
        f'{epic["hours"]:>2}h | '
        f'{epic["priority"]}'
    )

print("\nEpics:", len(data["epics"]))
print("Estimated hours:", total)
print("Jira changes: 0")
print("\nDRY-RUN: OK")
