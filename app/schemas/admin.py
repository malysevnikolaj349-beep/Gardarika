from pydantic import BaseModel


class DashboardStats(BaseModel):
    online: int
    economy_gold: int
    new_players: int
    server_load: int
    level_cap: int
    leader_name: str
    leader_level: int


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
    auction_tax: int
    npc_buy_multiplier: float


class WorldState(BaseModel):
    time_mode: str
    time_of_day: str
    weather: str
    season: str


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
