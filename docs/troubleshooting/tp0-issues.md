# TP0 — Issues and Resolutions

## Jira URL Typo
Issue: Jira URL initially used `atlassain.net`.

Resolution: corrected to `atlassian.net`.

## Jira Scoped Token Authentication
Issue: scoped API token returned HTTP 401 with scope mismatch.

Resolution: switched to a Classic API token. Authentication returned HTTP 200.

## Jira Hierarchy Assumption
Issue: initial design assumed Feature could parent Task.

Root cause: Jira discovery showed Feature and Task are both hierarchy level 0.

Resolution: use supported Jira hierarchy and avoid invalid parent relationships.

## Incomplete Jira Metadata
Issue: initial tickets lacked execution metadata.

Resolution: discovery and synchronization scripts populated assignment, priority, sprint, dates, estimates, story points, worklogs and final status.

## Sample Jira Tickets
Issue: SCRUM-3 and SCRUM-4 were temporary test tickets.

Resolution: removed during TP0 synchronization.

## Work Time Calculation
Gross session: 3h47.

Break: 15 minutes.

Net Jira worklog: 3h32.

## Missing tree Command
Issue: `tree` was not installed in Ubuntu.

Resolution: used the standard `find` command instead of adding an unnecessary dependency.

## Duplicate Backlog Risk
Issue: `create_backlog.py` is not currently idempotent.

Risk: rerunning it can create duplicate Jira issues.

Resolution: do not rerun blindly. Idempotency is a future automation improvement.

## Documentation Here-Document Failure
Issue: a large Bash here-document paste left the terminal waiting at the `>` continuation prompt.

Resolution: cancelled with Ctrl+C and switched to controlled generation through a Python documentation script.
