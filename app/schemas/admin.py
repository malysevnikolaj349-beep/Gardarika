from pydantic import BaseModel


class DashboardStats(BaseModel):
    online: int | None = None
    economy_gold: int | None = None
    new_players: int | None = None
    server_load: int | None = None
    level_cap: int | None = None
    leader_name: str | None = None
    leader_level: int | None = None


class PendingTrade(BaseModel):
    id: int
    seller: str
    buyer: str
    item: str
    price: int
    deviation: float
    status: str


class GuildReport(BaseModel):
    id: int
    player: str
    reason: str
    status: str


class EconomySettings(BaseModel):
    auction_tax: int | None = None
    npc_buy_multiplier: float | None = None


class WorldState(BaseModel):
    time_mode: str | None = None
    time_of_day: str | None = None
    weather: str | None = None
    season: str | None = None


class WorldEvent(BaseModel):
    id: int
    name: str
    status: str


class PlayerProfile(BaseModel):
    player_id: int
    nickname: str
    level: int
    gold: int
    experience: int
    is_pk: bool
    is_vip: bool
    in_jail: bool
    inventory: list[str]


class ClanSummary(BaseModel):
    id: int
    name: str
    leader: str
    treasury: int
    building_level: int


class TerritorySummary(BaseModel):
    id: int
    mine: str
    owner: str


class QuestStatus(BaseModel):
    id: int
    name: str
    status: str


class ActionLog(BaseModel):
    id: int
    category: str
    description: str


class AdminLog(BaseModel):
    id: int
    admin: str
    action: str
    created_at: str
