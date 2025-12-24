from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .models import ItemInstance, LootPile


@dataclass
class LootSplit:
    killer_visible: List[ItemInstance]
    ground_pile: LootPile
    hidden: List[ItemInstance]


def split_player_death_loot(
    location_id: str, x: int, y: int, dropped_items: List[ItemInstance]
) -> LootSplit:
    """Split death loot into killer-visible, ground, and hidden parts.

    The split is deterministic: first item goes to killer-only visibility, second
    is dropped publicly on the ground, the rest are hidden (but still exist for mobs
    to pick up). This avoids inventing probabilistic mechanics while satisfying the
    visibility constraints from the contract.
    """

    killer_visible: List[ItemInstance] = []
    ground_visible: List[ItemInstance] = []
    hidden: List[ItemInstance] = []

    for idx, item in enumerate(dropped_items):
        if idx == 0:
            killer_visible.append(item)
        elif idx == 1:
            ground_visible.append(item)
        else:
            hidden.append(item)

    pile = LootPile(
        location_id=location_id,
        x=x,
        y=y,
        visibility_mode="public",
        items=ground_visible,
    )
    return LootSplit(killer_visible=killer_visible, ground_pile=pile, hidden=hidden)

