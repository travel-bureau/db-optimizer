import os

from pymongo import MongoClient


def initialize_mongodb():
    global db
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGODB_DB_NAME")]

    print("Mongodb initialized!")

def delete_old_records(collection_name, threshold, delete_pct):
    collection = db[collection_name]
    delete_count = int(threshold * delete_pct)

    total_docs = collection.count_documents({})
    print(f"📊 Total documents in '{collection_name}': {total_docs}")

    if total_docs > threshold:
        print(f"⚠️ Threshold exceeded ({threshold}). Deleting {delete_count} oldest records...")

        # Sort by created_at ascending and delete the oldest
        old_docs = collection.find().sort("created_at", 1).limit(delete_count)
        ids_to_delete = [doc["_id"] for doc in old_docs]

        result = collection.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"✅ Deleted {result.deleted_count} records.")
    else:
        print("✅ No cleanup needed.")

