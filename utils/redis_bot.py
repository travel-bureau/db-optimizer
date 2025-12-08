import os

import redis

def initialize_redis():
    global redis_client
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        decode_responses=False,
        username=os.getenv("REDIS_USERNAME"),
        password=os.getenv("REDIS_PASSWORD"),
    )

    print("Redis initialized!")

def delete_keys_by_oldest_ttl(threshold, delete_pct):
    keys = redis_client.keys("*")
    total_keys = len(keys)
    print(f"📊 Total Redis keys: {total_keys}")

    delete_count = int(threshold * delete_pct)

    if total_keys > threshold:
        print(f"⚠️ Threshold exceeded ({threshold}). Deleting {delete_count} keys with shortest TTL...")

        ttl_map = []
        for key in keys:
            ttl = redis_client.ttl(key)
            if ttl >= 0:  # Only consider keys with expiration
                ttl_map.append((key, ttl))

        # Sort by TTL ascending (shortest remaining time first)
        ttl_map.sort(key=lambda x: x[1])
        keys_to_delete = [k.decode() if isinstance(k, bytes) else k for k, _ in ttl_map[:delete_count]]

        if keys_to_delete:
            redis_client.delete(*keys_to_delete)
            print(f"✅ Deleted {len(keys_to_delete)} keys.")
        else:
            print("⚠️ No expiring keys found to delete.")
    else:
        print("✅ No cleanup needed.")
