import asyncio
import tornado.web

from backend.db.db import PORT
from backend.handlers.matches import MatchHandler, MatchDeleteHandler
from backend.handlers.matches_fun import background_match_generator, background_match_time_updater, load_matches_from_db


def make_app():
    return tornado.web.Application(
        [

            (r"/api/matches", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})/delete", MatchDeleteHandler),

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "frontend"}),
            (r"/", tornado.web.RedirectHandler, {"url": "/static/main_page.html"}),
        ],
        autoreload=True,
        debug=True
    )


async def main(shutdown_event):
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")
    
    # Carica i match dal database all'avvio
    await load_matches_from_db()
    
    # Avvia il generatore di match in background
    generator_task = asyncio.create_task(background_match_generator(shutdown_event, championship="Champions League"))
    
    # Avvia l'aggiornatore di tempo dei match in background
    time_updater_task = asyncio.create_task(background_match_time_updater(shutdown_event, interval=1))
    
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()

