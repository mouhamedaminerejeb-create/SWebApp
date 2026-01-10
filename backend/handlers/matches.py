import tornado.escape

from backend.handlers.base import BaseHandler
from db.db import db_interface


class MatchHandler(BaseHandler):
    async def get(self):
        team=self.get_query_argument("teams",None)
        if team:
            matches = await db_interface.get_matches_by_team(team)
        out = [{
            "id": str(t["_id"]),
            "team1_name": await db_interface.get_team_by_id(t["team1_id"]).teamName,
            "team2_name": await db_interface.get_team_by_id(t["team2_id"]).teamName,
            "time": t["time"],
            "scoreT1": t["scoreT1"],
            "scoreT2": t["scoreT2"],
            "pointsT1": t["pointsT1"],
            "pointsT2": t["pointsT2"],
            "breaks": t["breaks"],
            "championship": t["championship"],
            "done": t["done"]

        } for t in matches]

        return self.write_json({"items": out})

    async def post(self):

        body = tornado.escape.json_decode(self.request.body)
        team1_id = body.get("team1_id", "").strip()
        team2_id = body.get("team2_id", "").strip()
        championship = body.get("championship", "").strip()

        if not team1_id:
            return self.write_json({"error": "Squadra obbligatorio"}, 400)

        if not team2_id:
            return self.write_json({"error": "Squadra obbligatorio"}, 400)
        
        if not championship:
            return self.write_json({"error": "Campionato obbligatorio"}, 400)

        result = await db_interface.create_match(team1_id,team2_id,championship)
        return self.write_json({"id": str(result.inserted_id)}, 201)


class MatchUpdateHandler(BaseHandler):
    async def put(self, match_id):
        if not match_id:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        done = body.get("done")

        await db_interface.update_task_done(match_id, done)
        return self.write_json({"message": "Aggiornato"})


class MatchDeleteHandler(BaseHandler):
    async def delete(self, match_id):
        if not match_id:
            return self.write_json({"error": "Match non definito"}, 401)

        await db_interface.delete_match(match_id)
        return self.write_json({"message": "Eliminato"})

