import os
from dotenv import load_dotenv
from pymongo import MongoClient


def load_db():
    # 1. Load environment variables (Local development look for a .env file; Render ignores this line)
    load_dotenv()

    # 2. Fetch the URI from the environment
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/local_db")

    # 3. Connect to the client
    client = MongoClient(MONGO_URI)

    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Database connection failed: {e}")

    return client