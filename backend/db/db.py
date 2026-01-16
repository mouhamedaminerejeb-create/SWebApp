from pymongo import AsyncMongoClient
from .db_interface import DatabaseInterface

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "sport_app_db"

PORT = 8888

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

db_interface = DatabaseInterface(db)