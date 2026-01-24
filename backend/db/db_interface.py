from bson import ObjectId


class DatabaseInterface:
    def __init__(self, db):
        self._teams = db.teams
        self._matches = db.matches

    # ---------- teams ----------

    async def get_all_teams(self):
        cursor = self._teams.find({})
        return [t async for t in cursor]

    async def get_team_by_name(self, teamName: str):
        return await self._teams.find_one({"teamName": teamName})
    
    async def get_team_by_id(self, team_id: str):
        return await self._teams.find_one({"_id": ObjectId(team_id)})

    async def create_team(self, teamName: str,teamAcronym: str, sport: str, players: list):
        return await self._teams.insert_one({
            "teamName": teamName,
            "teamAcronym": teamAcronym,
            "sport": sport,
            "players": players
        })

    # matches

    async def get_all_matches(self):
        cursor = self._matches.find({})
        return [t async for t in cursor]

    async def get_matches_by_team(self, team_id: str):
        cursor = self._matches.find({"$or": [{"team1_id": ObjectId(team_id)}, {"team2_id": ObjectId(team_id)}]})
        return [t async for t in cursor]

    async def create_match(self, team1_id: str, team2_id: str, championship:str):
        return await self._matches.insert_one({
            "team1_id": ObjectId(team1_id),
            "team2_id": ObjectId(team2_id),
            "scoreT1": [{"0": 0}],
            "scoreT2": [{"0": 0}],
            "pointsT1": 0,
            "pointsT2": 0,
            "breaks": [],
            "championship":championship,
            "time": 0,
            "done": False
        })
    
    async def generate_match(self, team1_id: str, team2_id: str, championship: str):
        team1 = await self.get_team_by_id(team1_id)
        team2 = await self.get_team_by_id(team2_id)
        if not team1:
            return self.write_json({"error": f"Squadra con ID {team1_id} non trovata"}, 400)
        if not team2:
            return self.write_json({"error": f"Squadra con ID {team2_id} non trovata"}, 400)
        if team1_id == team2_id:
            return self.write_json({"error": "Non puoi creare un match tra la stessa squadra"}, 400)
        result = await self.create_match(team1_id, team2_id, championship)
        match = await self._matches.find_one({"_id": result.inserted_id})
        return match
    
    async def update_match_scoreT1(self, match_id: str, scoreT1: list):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"scoreT1": list(scoreT1)}}
        )
    
    async def update_match_scoreT2(self, match_id: str, scoreT2: list):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"scoreT2": list(scoreT2)}}
        )
    
    async def update_match_pointsT1(self, match_id: str, pointsT1: int):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"pointsT1": int(pointsT1)}}
        )
    
    async def update_match_pointsT2(self, match_id: str, pointsT2: int):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"pointsT2": int(pointsT2)}}
        )

    async def update_match_breaks(self, match_id: str, breaks: list):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"breaks": list(breaks)}}
        )
    
    async def update_match_time(self, match_id: str, time: int):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"time": int(time)}}
        )
    
    async def update_match_done(self, match_id: str, done: bool):
        return await self._matches.update_one(
            {
                "_id": ObjectId(match_id)
            },
            {"$set": {"done": bool(done)}}
        )

    async def delete_match(self, match_id: str):
        return await self._matches.delete_one({
            "_id": ObjectId(match_id)
        })
