from tasks.domain.transform_file import transform_to_domain
from tasks.processed.enrich_file import enrich_data
from tasks.processed.ingest_to_db import ingest_to_db


def run():
    print("🚀 Running Pipeline...", flush=True)
    print("📌 Running domain transformation...", flush=True)
    try:
        transform_to_domain()
        print("✅ Successfully transformed to domain!", flush=True)
        enrich_data()
        print("✅ Successfully enriched data!", flush=True)
        print("📌 Ingesting file to the database...", flush=True)
        ingest_to_db()
        print("✅ Successfully ingested to database!", flush=True)
    except Exception as e:
        print(f"❌ Error running during transformation: {e}", flush=True)


if __name__ == "__main__":
    run()