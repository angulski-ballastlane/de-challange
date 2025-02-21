import json
from pymongo import MongoClient
from config import get_file_path,config

# Constants
MONGO_URI = config['database']['uri']
DB_NAME = config['database']['database_name']
COLLECTION_NAME = config['database']['collection_name']
FILE_PATH = get_file_path("processed", "enhanced_data")


#############
####MAIN#####
#############
def ingest_to_db():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            documents = data
        else:
            documents = [data]

        inserted_count = 0
        updated_count = 0
        for doc in documents:
            if "program_id" not in doc:
                print(f"⚠️ Skipping document without 'program_id': {doc}")
                continue
            # Delete old record if it exists and insert the new one
            result = collection.replace_one(
                {"program_id": doc["program_id"]},
                doc,
                upsert=True,
            )
            if result.matched_count > 0:
                updated_count += 1
                print(f"Updated document with program_id={doc['program_id']}.")
            else:
                inserted_count += 1
                print(f"Inserted new document with program_id={doc['program_id']}.")

        print(f"Total inserted: {inserted_count} | Total updated: {updated_count}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

    finally:
        client.close()
