from pymongo import AsyncMongoClient
from .db_interface import DatabaseInterface

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "sport_app"

COOKIE_SECRET = "super_secret_key_change_me"
PORT = 8888

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

db_interface = DatabaseInterface(db)