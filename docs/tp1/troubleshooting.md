# TP1 Troubleshooting

## PostgreSQL Bootstrap Conflict

Cause:
An obsolete initialization script created an incompatible product dataset,
causing downstream foreign-key loading problems.

Resolution:
The obsolete bootstrap was removed and the development database was rebuilt.

Prevention:
Database initialization scripts must be version-controlled and validated
against the active source contract.

## Python Virtual Environment

Cause:
The Ubuntu environment did not initially contain the required Python venv
package.

Resolution:
The required Ubuntu package was installed and the project virtual
environment was recreated.

## Support Validation Performance

Cause:
Ticket validation repeatedly scanned the complete order-line dataset.

Resolution:
A precomputed set was introduced for constant-time relationship lookup.

Prevention:
Large referential validations must use indexed/set-based lookups.

## Supply Chain Source Path

Cause:
The generator expected the warehouse master in an incorrect directory.

Resolution:
The source path was corrected to the canonical supply-chain location.

Prevention:
Source locations must be defined centrally through configuration/catalogs.

## PostgreSQL Shell Credentials

Cause:
PostgreSQL environment variables were not loaded into the active shell.

Resolution:
The project `.env` was loaded without displaying secrets.
