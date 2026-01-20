from pymongo import AsyncMongoClient
from db_interface import DatabaseInterface
import os
class DBPool:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

        # Load configuration from environment variables
        self.mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.mongo_port = int(os.getenv("MONGO_PORT", "27017"))
        self.mongo_user = os.getenv("MONGO_USER", "admin")
        self.mongo_password = os.getenv("MONGO_PASSWORD", "password")
        self.mongo_db = os.getenv("MONGO_DB", "sport_app_db")
        self.mongo_collection1 = os.getenv("MONGO_DB_COLLECTION1", "teams")
        self.mongo_collection2 = os.getenv("MONGO_DB_COLLECTION2", "matches")

    async def connect(self):
        DB_CONNECTION_STRING = f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"
        self.client = AsyncMongoClient(DB_CONNECTION_STRING,
                                       maxPoolSize = 20,
                                       minPoolSize = 5,
                                       maxIdleTimeMS = 30000)
        self.db = self.client[self.mongo_db]
        self.collection1 = self.db[self.mongo_collection1]
        self.collection2 = self.db[self.mongo_collection2]
        print("client connected to MongoDB service")

    async def close(self):
        if self.client:
            self.client.close()