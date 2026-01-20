import tornado.escape
import asyncio
import random
from bson import ObjectId

from backend.handlers.base import BaseHandler
from backend.handlers.matches_fun import matches_cache,teams_cache,is_team_in_active_match,load_matches_from_db,load_teams,background_match_generator,background_match_time_updater
from backend.db import db_interface

class MatchHandler(BaseHandler):
    async def get(self):
            out = []
            for match in matches_cache.values():
                out.append({
                    "id": str(match["_id"]),
                    "team1_name": match["team1_name"],
                    "team2_name": match["team2_name"],
                    "time": match["time"],
                    "scoreT1": match["scoreT1"],
                    "scoreT2": match["scoreT2"],
                    "pointsT1": match["pointsT1"],
                    "pointsT2": match["pointsT2"],
                    "breaks": match["breaks"],
                    "championship": match["championship"],
                    "done": match["done"]
                })

            return self.write_json({"items": out})

    async def post(self):
            body = tornado.escape.json_decode(self.request.body)
            championship = body.get("championship", "").strip()
            if not championship:
                return self.write_json({"error": "Campionato obbligatorio"}, 400)
            teams = await db_interface.get_all_teams()
            if len(teams) < 2:
                return self.write_json({"error": "Servono almeno 2 squadre nel database"}, 400)
            team1, team2 = random.sample(teams, 2)
            match = await db_interface.generate_match(str(team1["_id"]),str(team2["_id"]),championship)
            team1_data = await db_interface.get_team_by_id(str(match["team1_id"]))
            team2_data = await db_interface.get_team_by_id(str(match["team2_id"]))
            
            return self.write_json({
                "id": str(match["_id"]),
                "team1_name": team1_data["teamName"],
                "team2_name": team2_data["teamName"],
                "time": match["time"],
                "scoreT1": match["scoreT1"],
                "scoreT2": match["scoreT2"],
                "pointsT1": match["pointsT1"],
                "pointsT2": match["pointsT2"],
                "breaks": match["breaks"],
                "championship": match["championship"],
                "done": match["done"]
            }, 201)

class MatchDeleteHandler(BaseHandler):
    async def delete(self, match_id):
        try:
            if not match_id:
                return self.write_json({"error": "Match non definito"}, 401)

            await db_interface.delete_match(match_id)
            return self.write_json({"message": "Eliminato"})
        except Exception as e:
            return self.write_json({"error": str(e)}, 400)