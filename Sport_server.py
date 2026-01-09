import asyncio
import tornado.web

from backend.db.db import COOKIE_SECRET, PORT
from backend.handlers.matches import MatchHandler, MatchUpdateHandler, MatchDeleteHandler


def make_app():
    return tornado.web.Application(
        [

            (r"/api/matches", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})", MatchHandler),
            (r"/api/matches/([a-f0-9]{24})/edit", MatchUpdateHandler),
            (r"/api/matches/([a-f0-9]{24})/delete", MatchDeleteHandler),

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
            (r"/", tornado.web.RedirectHandler, {"url": "/static/main_page.html"}),
        ],
        cookie_secret=COOKIE_SECRET,
        autoreload=True,
        debug=True
    )


async def main(shutdown_event):
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")
    await shutdown_event.wait()
    print("Chiusura server...")


if __name__ == "__main__":
    shutdown_event = asyncio.Event()
    try:
        asyncio.run(main(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()

