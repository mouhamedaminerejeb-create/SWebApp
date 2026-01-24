import tornado.escape
import asyncio
import random
from bson import ObjectId

from backend.handlers.base import BaseHandler

matches_cache = {}
teams_cache = None
db_int=None

events=["goal1","goal2","fallo","pausa"]

def is_team_in_active_match(team_id):
    for match in matches_cache.values():
        if not match["done"]:  
            if str(match["team1_id"]) == str(team_id) or str(match["team2_id"]) == str(team_id):
                return True
    return False

async def load_teams(DbI):
    global teams_cache
    global db_int
    db_int=DbI

    teams_cache = await db_int.get_all_teams()
    return teams_cache

async def load_matches_from_db():
    global matches_cache
    try:
        all_matches = await db_int.get_all_matches()
        matches_cache.clear()
        
        for match_db in all_matches:
            match_id = str(match_db["_id"])
            team1_id = str(match_db["team1_id"])
            team2_id = str(match_db["team2_id"])
            
            team1_data = await db_int.get_team_by_id(team1_id)
            team2_data = await db_int.get_team_by_id(team2_id)
            
            matches_cache[match_id] = {
                "_id": match_db["_id"],
                "team1_id": match_db["team1_id"],
                "team2_id": match_db["team2_id"],
                "team1_name": team1_data["teamName"],
                "team2_name": team2_data["teamName"],
                "scoreT1": match_db["scoreT1"],
                "scoreT2": match_db["scoreT2"],
                "pointsT1": match_db["pointsT1"],
                "pointsT2": match_db["pointsT2"],
                "breaks": match_db["breaks"],
                "championship": match_db["championship"],
                "time": match_db["time"],
                "done": match_db["done"]
            }
        
        print(f"Caricati {len(matches_cache)} match dalla database")
    except Exception as e:
        print(f"Errore nel caricamento dei match dal database: {e}")

async def background_match_time_updater(shutdown_event, interval=1):
    while not shutdown_event.is_set():
        try:
            for match_id, match in matches_cache.items():
                #print(match["done"])
                if not match["done"]:
                    if match["time"] >= 90:
                        match["done"] = True
                        if next(iter(match["scoreT1"][-1]))==next(iter(match["scoreT2"][-1])):
                            match["pointsT1"]+=1
                            match["pointsT2"]+=1

                        elif next(iter(match["scoreT1"][-1]))>next(iter(match["scoreT2"][-1])):
                            match["pointsT1"]+=2

                        elif next(iter(match["scoreT1"][-1]))<next(iter(match["scoreT2"][-1])):
                            match["pointsT2"]+=2
                        await db_int.update_match_scoreT1(match_id,match["scoreT1"])
                        await db_int.update_match_scoreT2(match_id,match["scoreT2"])
                        await db_int.update_match_pointsT1(match_id,match["pointsT1"])
                        await db_int.update_match_pointsT2(match_id,match["pointsT2"])
                        await db_int.update_match_done(match_id, True)
                        await db_int.update_match_time(match_id, match["time"])
                    else:
                        probabilita=random.randint(0,100)
                        if probabilita>=90:
                            pulled_event = random.choice(events)
                            if pulled_event == "goal1":
                                last_key = next(iter(match["scoreT1"][-1]))
                                match["scoreT1"].append({str(int(last_key) + 1): match["time"]})
                            elif pulled_event == "goal2":
                                last_key = next(iter(match["scoreT2"][-1]))
                                match["scoreT2"].append({str(int(last_key) + 1): match["time"]})
                            elif pulled_event=="fallo":
                                match["breaks"].append({"fallo":match["time"]})
                            elif pulled_event=="pausa":
                                match["breaks"].append({"pausa":match["time"]})

                        match["time"] = match.get("time") + 1
                        
            active_matches = len([m for m in matches_cache.values() if not m.get("done")])
            if active_matches > 0:
                print(f"{active_matches} Match in corso")
        except Exception as e:
            print(f"Errore nell'aggiornamento del tempo: {e}")
        try:
            await asyncio.wait_for(shutdown_event.wait(), timeout=interval)
            break
        except asyncio.TimeoutError:
            pass

async def background_match_generator(shutdown_event, championship="Serie A"):
    global teams_cache
    print(len(teams_cache))
    print(f"Generatore di match avviato - Campionato: {championship}")
    while not shutdown_event.is_set():
        interval = random.randint(5, 20)
        try:
            if len(teams_cache) >= 2:
                available_teams = [t for t in teams_cache if not is_team_in_active_match(str(t["_id"]))]
                print(len(available_teams))
                if len(available_teams) >= 2:
                    team1, team2 = random.sample(available_teams, 2)
                    try:
                        match_db = await db_int.generate_match(
                            str(team1["_id"]),
                            str(team2["_id"]),
                            championship
                        )

                        match_id = str(match_db["_id"])
                        matches_cache[match_id] = {
                            "_id": match_db["_id"],
                            "team1_id": match_db["team1_id"],
                            "team2_id": match_db["team2_id"],
                            "team1_name": team1["teamName"],
                            "team2_name": team2["teamName"],
                            "scoreT1": [{"0": 0}],
                            "scoreT2": [{"0": 0}],
                            "pointsT1": 0,
                            "pointsT2": 0,
                            "time": 0,
                            "breaks": [],
                            "championship": championship,
                            "done": False
                        }
                        print(f"✓ Match generato: {team1['teamName']} vs {team2['teamName']}")
                    except Exception as e:
                        print(f"Errore nella generazione del match: {e}")
            else:
                print("Attenzione: servono almeno 2 squadre nel database")
                
        except Exception as e:
            print(f"Errore nel generatore di match: {e}")
        try:
            await asyncio.wait_for(shutdown_event.wait(), timeout=interval)
            break
        except asyncio.TimeoutError:
            pass
