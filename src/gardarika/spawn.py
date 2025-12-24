from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SpawnChoice:
    city_id: str
    name: str
    spawn_enabled: bool
    spawn_capacity: int
    population: Dict[str, int]


def select_home_city(available_cities: List[SpawnChoice], fallback_city_id: str) -> str:
    """Pick a home city for a new player respecting spawn_enabled flag.

    The contract requires first players to default to the novice city when no other
    spawn options are available. When several cities are open, the first spawn_enabled
    entry is chosen deterministically to avoid improvisation here.
    """

    for city in available_cities:
        if city.spawn_enabled and city.spawn_capacity > 0:
            return city.city_id
    return fallback_city_id

