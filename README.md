# 🧹 MongoDB & Redis Record Cleaner

This Python script monitors MongoDB collections and Redis keys, automatically deleting old records when threshold limits are exceeded. It's designed for environments where data volume needs to be controlled without manual intervention.

---

## 🚀 Features

- ✅ Tracks multiple MongoDB collections
- ✅ Monitors Redis keys and TTLs
- ✅ Deletes oldest records when thresholds are breached
- ✅ Configurable limits per collection or key pattern
- ✅ Audit-safe logging for every deletion
- ✅ Lightweight and easy to integrate into cron jobs or CI/CD pipelines

---

## 🛠️ Requirements

- Python 3.7+
- `pymongo`
- `redis`
- Optional: `python-dotenv` for environment variable management

Install dependencies:

```bash
pip install pymongo redis python-dotenv
```

---

## ⚙️ Configuration

Set your environment variables in a .env file or directly in your shell:
```commandline
MONGO_URI=mongodb://localhost:27017
MONGO_DB=my_database

REDIS_HOST=localhost
REDIS_PORT=6379

THRESHOLD_COLLECTION_users=10000
THRESHOLD_COLLECTION_logs=50000
THRESHOLD_REDIS_pattern_user:*_session=1000
```

---

## 📦 Usage

Run the script manually or schedule it:

```bash
python main.py
```

Or add to a cron job:

```bash
0 * * * * /usr/bin/python /path/to/cleanup.py >> /var/log/db_cleanup.log 2>&1
```

## 🧠 How It Works

- MongoDB: For each collection with a threshold, the script counts documents and deletes the oldest ones (based on _id or created_at) if the count exceeds the limit.
- Redis: For each key pattern, it counts matching keys and deletes the oldest or least recently used keys if the count exceeds the limit.

## 📋 Sample Output

```commandline
✅ users: 12,340 documents → deleted 2,340 oldest
✅ Redis keys matching user:*_session: 1,200 → deleted 200 keys
```

## 🛡️ Safety Notes

- This script performs irreversible deletions. Use with caution in production.
- Consider running in dry-run mode first (optional flag can be added).

## 🤝 Contributing
Feel free to submit issues or PRs to improve configurability, add dry-run support, or enhance logging.

