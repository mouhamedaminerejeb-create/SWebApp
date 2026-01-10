import asyncio
import json
from pymongo import AsyncMongoClient

# docker start -it mongodb mongosh
# use sport_app_db

async def main():
    client = AsyncMongoClient("mongodb://localhost:27017")
    db = client["sport_app_db"]
    teams_collection = db["teams"]
    matches_collection = db["matches"]

    with open("backend/db/teams.json", "r", encoding="utf-8") as f:
        team_data = json.load(f)

    with open("backend/db/matches.json", "r", encoding="utf-8") as f:
        match_data = json.load(f)

    print("Svuoto la collezione")
    await teams_collection.delete_many({})
    await matches_collection.delete_many({})

    print("Inserisco i documenti")
    result = await teams_collection.insert_many(team_data)
    result = await matches_collection.insert_many(match_data)

    print(f"Inseriti {len(result.inserted_ids)} documenti.")
    print("Operazione completata")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())