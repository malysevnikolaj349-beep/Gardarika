from aiohttp import web

from app.core.config import settings
from app.schemas.admin import EconomySettings


def _require_auth(request: web.Request) -> None:
    token = request.query.get("token") or request.headers.get("X-Admin-Token")
    if token != settings.admin_webapp_token:
        raise web.HTTPUnauthorized(text="Invalid token")


async def index(request: web.Request) -> web.Response:
    _require_auth(request)
    return web.FileResponse(path="app/web/templates/index.html")


async def static_file(request: web.Request) -> web.Response:
    return web.FileResponse(path=f"app/web/static/{request.match_info['filename']}")


async def dashboard_stats(request: web.Request) -> web.Response:
    _require_auth(request)
    dashboard = request.app["dashboard"]
    stats = await dashboard.get_stats()
    return web.json_response(stats.model_dump())


async def force_new_epoch(request: web.Request) -> web.Response:
    _require_auth(request)
    dashboard = request.app["dashboard"]
    stats = await dashboard.force_new_epoch()
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", "Force new epoch")
    return web.json_response(stats.model_dump())


async def pending_trades(request: web.Request) -> web.Response:
    _require_auth(request)
    economy = request.app["economy"]
    trades = await economy.list_pending_trades()
    return web.json_response([trade.model_dump() for trade in trades])


async def update_trade(request: web.Request) -> web.Response:
    _require_auth(request)
    trade_id = int(request.match_info["trade_id"])
    data = await request.json()
    status = data.get("status", "pending")
    economy = request.app["economy"]
    await economy.update_trade_status(trade_id, status)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Trade {trade_id} -> {status}")
    return web.json_response({"status": "ok"})


async def guild_reports(request: web.Request) -> web.Response:
    _require_auth(request)
    economy = request.app["economy"]
    reports = await economy.list_guild_reports()
    return web.json_response([report.model_dump() for report in reports])


async def update_guild_report(request: web.Request) -> web.Response:
    _require_auth(request)
    report_id = int(request.match_info["report_id"])
    data = await request.json()
    status = data.get("status", "open")
    economy = request.app["economy"]
    await economy.update_guild_report(report_id, status)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Guild report {report_id} -> {status}")
    return web.json_response({"status": "ok"})


async def economy_settings(request: web.Request) -> web.Response:
    _require_auth(request)
    economy = request.app["economy"]
    settings_data = await economy.get_settings()
    return web.json_response(settings_data.model_dump())


async def update_economy_settings(request: web.Request) -> web.Response:
    _require_auth(request)
    economy = request.app["economy"]
    data = await request.json()
    new_settings = await economy.update_settings(
        auction_tax=int(data.get("auction_tax", 5)),
        npc_buy_multiplier=float(data.get("npc_buy_multiplier", 1.0)),
    )
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", "Updated economy settings")
    return web.json_response(new_settings.model_dump())


async def world_state(request: web.Request) -> web.Response:
    _require_auth(request)
    world = request.app["world"]
    state = await world.get_state()
    return web.json_response(state.model_dump())


async def update_world_state(request: web.Request) -> web.Response:
    _require_auth(request)
    world = request.app["world"]
    data = await request.json()
    state = await world.update_state(
        time_mode=data.get("time_mode"),
        time_of_day=data.get("time_of_day"),
        weather=data.get("weather"),
        season=data.get("season"),
    )
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", "Updated world state")
    return web.json_response(state.model_dump())


async def world_events(request: web.Request) -> web.Response:
    _require_auth(request)
    world = request.app["world"]
    events = await world.list_events()
    return web.json_response([event.model_dump() for event in events])


async def trigger_world_event(request: web.Request) -> web.Response:
    _require_auth(request)
    event_id = int(request.match_info["event_id"])
    world = request.app["world"]
    await world.trigger_event(event_id)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Triggered event {event_id}")
    return web.json_response({"status": "ok"})


async def player_search(request: web.Request) -> web.Response:
    _require_auth(request)
    query = request.query.get("q", "")
    players = request.app["players"]
    profile = await players.find_player(query)
    if not profile:
        raise web.HTTPNotFound(text="Player not found")
    return web.json_response(profile.model_dump())


async def update_player(request: web.Request) -> web.Response:
    _require_auth(request)
    player_id = int(request.match_info["player_id"])
    data = await request.json()
    players = request.app["players"]
    await players.update_player(
        player_id=player_id,
        level=data.get("level"),
        gold=data.get("gold"),
        experience=data.get("experience"),
        is_pk=data.get("is_pk"),
        is_vip=data.get("is_vip"),
        in_jail=data.get("in_jail"),
    )
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Updated player {player_id}")
    return web.json_response({"status": "ok"})


async def add_inventory_item(request: web.Request) -> web.Response:
    _require_auth(request)
    player_id = int(request.match_info["player_id"])
    data = await request.json()
    item = data.get("item", "")
    players = request.app["players"]
    await players.add_inventory_item(player_id, item)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Added item {item} to {player_id}")
    return web.json_response({"status": "ok"})


async def remove_inventory_item(request: web.Request) -> web.Response:
    _require_auth(request)
    player_id = int(request.match_info["player_id"])
    data = await request.json()
    item = data.get("item", "")
    players = request.app["players"]
    await players.remove_inventory_item(player_id, item)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Removed item {item} from {player_id}")
    return web.json_response({"status": "ok"})


async def clans(request: web.Request) -> web.Response:
    _require_auth(request)
    clans_service = request.app["clans"]
    clans_list = await clans_service.list_clans()
    return web.json_response([clan.model_dump() for clan in clans_list])


async def update_clan_leader(request: web.Request) -> web.Response:
    _require_auth(request)
    clan_id = int(request.match_info["clan_id"])
    data = await request.json()
    leader = data.get("leader", "")
    clans_service = request.app["clans"]
    await clans_service.update_leader(clan_id, leader)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Clan {clan_id} leader -> {leader}")
    return web.json_response({"status": "ok"})


async def territories(request: web.Request) -> web.Response:
    _require_auth(request)
    clans_service = request.app["clans"]
    territory_list = await clans_service.list_territories()
    return web.json_response([territory.model_dump() for territory in territory_list])


async def reset_territories(request: web.Request) -> web.Response:
    _require_auth(request)
    clans_service = request.app["clans"]
    await clans_service.reset_territories()
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", "Reset territories")
    return web.json_response({"status": "ok"})


async def quests(request: web.Request) -> web.Response:
    _require_auth(request)
    content = request.app["content"]
    quest_list = await content.list_quests()
    return web.json_response([quest.model_dump() for quest in quest_list])


async def reset_quest(request: web.Request) -> web.Response:
    _require_auth(request)
    quest_id = int(request.match_info["quest_id"])
    content = request.app["content"]
    await content.reset_legend(quest_id)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Reset quest {quest_id}")
    return web.json_response({"status": "ok"})


async def spawn_item(request: web.Request) -> web.Response:
    _require_auth(request)
    data = await request.json()
    player_id = int(data.get("player_id"))
    item = data.get("item", "")
    content = request.app["content"]
    await content.spawn_item(player_id, item)
    log_service = request.app["logs"]
    await log_service.add_admin_log("webapp", f"Spawned {item} for {player_id}")
    return web.json_response({"status": "ok"})


async def action_logs(request: web.Request) -> web.Response:
    _require_auth(request)
    logs = request.app["logs"]
    actions = await logs.list_action_logs()
    return web.json_response([action.model_dump() for action in actions])


async def admin_logs(request: web.Request) -> web.Response:
    _require_auth(request)
    logs = request.app["logs"]
    entries = await logs.list_admin_logs()
    return web.json_response([entry.model_dump() for entry in entries])


def setup_routes(app: web.Application) -> None:
    app.router.add_get("/", index)
    app.router.add_get("/static/{filename}", static_file)

    app.router.add_get("/api/dashboard", dashboard_stats)
    app.router.add_post("/api/dashboard/epoch", force_new_epoch)

    app.router.add_get("/api/economy/trades", pending_trades)
    app.router.add_post("/api/economy/trades/{trade_id}", update_trade)
    app.router.add_get("/api/economy/reports", guild_reports)
    app.router.add_post("/api/economy/reports/{report_id}", update_guild_report)
    app.router.add_get("/api/economy/settings", economy_settings)
    app.router.add_put("/api/economy/settings", update_economy_settings)

    app.router.add_get("/api/world/state", world_state)
    app.router.add_put("/api/world/state", update_world_state)
    app.router.add_get("/api/world/events", world_events)
    app.router.add_post("/api/world/events/{event_id}/trigger", trigger_world_event)

    app.router.add_get("/api/players/search", player_search)
    app.router.add_put("/api/players/{player_id}", update_player)
    app.router.add_post("/api/players/{player_id}/inventory", add_inventory_item)
    app.router.add_delete("/api/players/{player_id}/inventory", remove_inventory_item)

    app.router.add_get("/api/clans", clans)
    app.router.add_put("/api/clans/{clan_id}/leader", update_clan_leader)
    app.router.add_get("/api/territories", territories)
    app.router.add_post("/api/territories/reset", reset_territories)

    app.router.add_get("/api/content/quests", quests)
    app.router.add_post("/api/content/quests/{quest_id}/reset", reset_quest)
    app.router.add_post("/api/content/spawn", spawn_item)

    app.router.add_get("/api/logs/actions", action_logs)
    app.router.add_get("/api/logs/admin", admin_logs)
