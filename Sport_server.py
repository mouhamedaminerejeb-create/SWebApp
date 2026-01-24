import asyncio
import tornado.web

from backend.db.db import DBPool
from backend.handlers.matches import MatchHandler, MatchDeleteHandler
from backend.handlers.matches_fun import background_match_generator, background_match_time_updater, load_teams, load_matches_from_db
#docker compose up

def make_app():
    """Create the Tornado application with the shared pool"""
    return tornado.web.Application([
            (r"/api/matches", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})/delete", MatchDeleteHandler),

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "frontend"}),
            (r"/", tornado.web.RedirectHandler, {"url": "/static/main_page.html"}),
        ],
        autoreload=True,
        debug=True)

async def main(shutdown_event):
    db_pool = DBPool()
    await db_pool.connect()
    await load_teams(db_pool.db_inter)


    app = make_app()
    app.listen(8888)
    print("server listening on port 8888")

    await load_matches_from_db()
    generator_task = asyncio.create_task(background_match_generator(shutdown_event, championship="Serie A"))
    time_updater_task = asyncio.create_task(background_match_time_updater(shutdown_event, interval=1))

    try:
        await shutdown_event.wait()
    finally:
        await db_pool.close()
        print("\nserver stopped")

if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()


