from bson import ObjectId


class DatabaseInterface:
    def __init__(self, db):
        self._teams = db["teams"]
        self._matches = db["matches"]

    # ---------- USERS ----------

    async def get_team_by_name(self, teamName: str):
        return await self._teams.find_one({"teamName": teamName})
    
    async def get_team_by_id(self, team_id: str):
        return await self._teams.find_one({"_id": ObjectId(team_id)})

    async def create_team(self, teamName: str,teamAcronym: str, sport: str, players: list):
        return await self._users.insert_one({
            "teamName": teamName,
            "teamAcronym": teamAcronym,
            "sport": sport,
            "players": players
        })

    # TASKS

    async def get_matches_by_team(self, team_id: str):
        cursor = self._tasks.find({"team_id": ObjectId(team_id)})
        return [t async for t in cursor]

    async def create_match(self, team1_id: str, team2_id: str, time: int, championship:str):
        return await self._tasks.insert_one({
            "team1_id": ObjectId(team1_id),
            "team2_id": ObjectId(team2_id),
            "time":time,
            "scoreT1": 0,
            "scoreT2": 0,
            "pointsT1": 0,
            "pointsT2": 0,
            "breaks": [],
            "championship":championship,
            "done": False
        })
    

    async def update_match_time(self, match_id: str, time: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"time": str(time)}}
        )
    
    async def update_match_scoreT1(self, match_id: str, scoreT1: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"scoreT1": int(scoreT1)}}
        )
    
    async def update_match_scoreT2(self, match_id: str, scoreT2: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"scoreT2": int(scoreT2)}}
        )
    
    async def update_match_pointsT1(self, match_id: str, pointsT1: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"pointsT1": int(pointsT1)}}
        )
    
    async def update_match_pointsT2(self, match_id: str, pointsT2: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"pointsT2": int(pointsT2)}}
        )

    async def update_match_breaks(self, match_id: str, breaks: int):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"breaks": int(breaks)}}
        )
    
    async def update_match_done(self, match_id: str, done: bool):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"done": bool(done)}}
        )

    async def delete_match(self, match_id: str):
        return await self._tasks.delete_one({
            "_id": ObjectId(match_id)
        })

