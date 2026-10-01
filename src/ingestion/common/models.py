from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class IngestionMetadata:
    source: str
    source_type: str
    run_id: str
    record_count: int
    status: str
    ingestion_timestamp: str = ""

    def __post_init__(self):
        if not self.ingestion_timestamp:
            self.ingestion_timestamp = datetime.now(timezone.utc).isoformat()
