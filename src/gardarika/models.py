from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class BattleState(str, Enum):
    PREPARING = "preparing"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


@dataclass
class BattleEffect:
    name: str
    remaining_turns: int
    skip_turn: bool = False
    fear_chance: float = 0.0
    bleed_damage: int = 0

    def tick(self) -> None:
        if self.remaining_turns > 0:
            self.remaining_turns -= 1

    @property
    def expired(self) -> bool:
        return self.remaining_turns <= 0


@dataclass
class Skill:
    name: str
    energy_cost: int
    cooldown: int
    effects: List[BattleEffect] = field(default_factory=list)


@dataclass
class ItemDefinition:
    item_def_id: str
    name: str
    base_value: int
    is_unique: bool = False


@dataclass
class ItemInstance:
    item_def: ItemDefinition
    instance_id: str


@dataclass
class InventoryItem:
    owner_type: str
    owner_id: str
    slot: str
    item: ItemInstance
    quantity: int = 1


@dataclass
class Location:
    location_id: str
    world_x: int
    world_y: int
    biome: str
    owner_principality_id: Optional[str]
    is_safe_zone: bool
    pvp_policy: Optional[str] = None
    tax_policy: Optional[Dict[str, int]] = None


@dataclass
class LocationCell:
    location_id: str
    x: int
    y: int
    terrain_type: str
    flags_json: Dict[str, str] = field(default_factory=dict)


@dataclass
class LootPile:
    location_id: str
    x: int
    y: int
    visibility_mode: str  # public/killer_only/hidden
    items: List[ItemInstance] = field(default_factory=list)


@dataclass
class Player:
    tg_id: int
    player_id: str
    home_city_id: str
    current_location_id: str
    x: int
    y: int
    hp: int
    hp_max: int
    level: int
    xp: int
    fame: int
    fear: int
    energy_max: int = 10


@dataclass
class MobInstance:
    mob_instance_id: str
    mob_def_id: str
    unique_name: Optional[str]
    location_id: str
    x: int
    y: int
    hp_current: int
    level_current: int
    is_boss: bool = False
    is_important: bool = False
    fixed_drop_table: List[ItemDefinition] = field(default_factory=list)
    picked_items: List[ItemInstance] = field(default_factory=list)


@dataclass
class City:
    city_id: str
    name: str
    location_id: str
    owner_principality_id: Optional[str]
    state: str
    spawn_enabled: bool
    spawn_capacity: int
    population: Dict[str, int] = field(default_factory=dict)


@dataclass
class Principality:
    principality_id: str
    name: str
    treasury_value: int = 0


@dataclass
class Battle:
    battle_id: str
    location_id: str
    x: int
    y: int
    battle_type: str  # pve/pvp
    turn: int
    state: BattleState
    energy_available: Dict[str, int] = field(default_factory=dict)
    cooldowns: Dict[str, int] = field(default_factory=dict)
    effects: Dict[str, List[BattleEffect]] = field(default_factory=dict)
    participants_hp: Dict[str, int] = field(default_factory=dict)

    def start_participant(self, participant_id: str, energy_max: int, hp: int) -> None:
        """Ensure energy is full at start of battle."""
        self.energy_available[participant_id] = energy_max
        self.participants_hp[participant_id] = hp
        self.effects.setdefault(participant_id, [])

    def apply_effects_end_of_turn(self) -> None:
        for pid, effect_list in list(self.effects.items()):
            for eff in list(effect_list):
                if eff.bleed_damage:
                    self.participants_hp[pid] = max(0, self.participants_hp[pid] - eff.bleed_damage)
                eff.tick()
            self.effects[pid] = [e for e in effect_list if not e.expired]

