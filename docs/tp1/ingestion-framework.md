# TP1 Ingestion Framework

## Technology

Python 3 filesystem ingestion framework.

## Technique

Metadata-driven ingestion with SHA-256 fingerprints.

## Processing

1. Discover configured sources.
2. Validate source existence.
3. Calculate source checksum.
4. Detect unchanged datasets.
5. Preserve source representation in Raw.
6. Publish validated representation to Bronze.
7. Reconcile source and Bronze row counts.
8. Persist run metadata and logs.

## Idempotence

Unchanged sources are identified by SHA-256 checksum and skipped when their
Raw and Bronze representations already exist.

## Incremental Behavior

Changed source fingerprints trigger re-ingestion while unchanged datasets
remain untouched.

## Error Handling

A failed dataset prevents successful run completion.
Run metadata records failed execution state.

## Execution

From the repository root:

`python automation/tp1/run_tp1_core.py`
