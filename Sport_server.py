import asyncio
import tornado.web
import signal

from backend.db.db import DBPool
from backend.handlers.matches import MatchHandler, MatchDeleteHandler
from backend.handlers.matches_fun import background_match_generator, background_match_time_updater, load_matches_from_db
#docker compose up

def make_app(db_pool):
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

async def main():
    db_pool = DBPool()
    await db_pool.connect()

    app = make_app(db_pool)
    app.listen(8888)
    print("server listening on port 8888")

    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        print("\nshutting down server gracefully")
        shutdown_event.set()

    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await shutdown_event.wait()
    finally:
        await db_pool.close()
        print("\nserver stopped")

asyncio.run(main())


