import asyncio
import json
import os
from dotenv import load_dotenv

from utils.mongodb_bot import initialize_mongodb, delete_old_records
from utils.redis_bot import initialize_redis, delete_keys_by_oldest_ttl

load_dotenv()

initialize_mongodb()
initialize_redis()

# Load thresholds from JSON
with open(os.path.join("constants", "thresholds.json")) as f:
    config = json.load(f)

async def run_bot(request=None, source="local"):
    return await main(request, source)

def trigger(request):
    return asyncio.run(run_bot(request, source="gcp"))

async def main(request=None, source="local"):
    print(source)
    mongo_collections = config["mongo_db"]["collections"]
    redis_config = config["redis"]

    # Clear mongodb
    for col in mongo_collections:
        collection_name = col["name"]
        threshold = int(col["threshold"])
        del_pct = float(col["del_pct"])
        delete_old_records(collection_name, threshold, del_pct)

    # Clear redis
    threshold = int(redis_config["threshold"])
    del_pct = float(redis_config["del_pct"])

    delete_keys_by_oldest_ttl(threshold, del_pct)

    return "Done!!"

if __name__ == "__main__":
    asyncio.run(run_bot())