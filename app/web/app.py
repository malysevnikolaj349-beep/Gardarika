from aiohttp import web

from app.core.config import settings
from app.db.database import Database
from app.services.clans import ClanService
from app.services.content import ContentService
from app.services.dashboard import DashboardService
from app.services.economy import EconomyService
from app.services.logs import LogService
from app.services.players import PlayerService
from app.services.world import WorldService
from app.web.routes import setup_routes


class WebApp:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.app = web.Application()
        self.app["db"] = db
        self.app["dashboard"] = DashboardService(db)
        self.app["economy"] = EconomyService(db)
        self.app["world"] = WorldService(db)
        self.app["players"] = PlayerService(db)
        self.app["clans"] = ClanService(db)
        self.app["content"] = ContentService(db)
        self.app["logs"] = LogService(db)
        setup_routes(self.app)

    def run(self) -> web.AppRunner:
        return web.AppRunner(self.app)


async def start_web_app(db: Database) -> web.TCPSite:
    web_app = WebApp(db)
    runner = web_app.run()
    await runner.setup()
    site = web.TCPSite(runner, settings.webapp_host, settings.webapp_port)
    await site.start()
    return site
