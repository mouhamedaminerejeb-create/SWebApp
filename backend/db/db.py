from pymongo import AsyncMongoClient
from backend.db.db_interface import DatabaseInterface
import os

class DBPool:
    def __init__(self):

        self.client = None
        self.db = None
        self.teams = None
        self.matches = None
        self.db_inter=None

        # Load configuration from environment variables
        self.mongo_host = os.getenv("MONGO_HOST", "localhost")
        self.mongo_port = int(os.getenv("MONGO_PORT", "27017"))
        self.mongo_db = os.getenv("MONGO_DB", "sport_app_db")
        self.teams = os.getenv("MONGO_DB_COLLECTION1", "teams")
        self.matches = os.getenv("MONGO_DB_COLLECTION2", "matches")

        

    async def connect(self):
        global db_int
        DB_CONNECTION_STRING = f"mongodb://{self.mongo_host}:{self.mongo_port}"
        self.client = AsyncMongoClient(DB_CONNECTION_STRING,
                                       maxPoolSize = 20,
                                       minPoolSize = 5,
                                       maxIdleTimeMS = 30000)
        self.db = self.client[self.mongo_db]
        self.teams = self.db[self.matches]
        self.matches = self.db[self.matches]
        self.db_inter = DatabaseInterface(self.db)
        print("client connected to MongoDB service")

    async def close(self):
        if self.client:
            self.client.close()