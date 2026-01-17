import asyncio
import json
from pymongo import AsyncMongoClient

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

    print("Inserisco i team")
    teams_result = await teams_collection.insert_many(team_data)
    team_ids = teams_result.inserted_ids
    
    print(f"Inseriti {len(team_ids)} team")
    print(f"Team IDs: {team_ids}")
    for match in match_data:
        if "team1_id" in match and isinstance(match["team1_id"], dict) and "$oid" in match["team1_id"]:
            pass

    updated_match_data = []
    for i, match in enumerate(match_data):
        updated_match = match.copy()
        if i == 0:
            updated_match["team1_id"] = team_ids[0]
            updated_match["team2_id"] = team_ids[1]
        elif i == 1:
            updated_match["team1_id"] = team_ids[2]
            updated_match["team2_id"] = team_ids[3]
        updated_match_data.append(updated_match)

    print("Inserisco i match con gli ID corretti")
    #matches_result = await matches_collection.insert_many(updated_match_data)

    #print(f"Inseriti {len(matches_result.inserted_ids)} match.")
    print("Operazione completata")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())