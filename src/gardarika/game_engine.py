from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .models import Battle, BattleEffect, BattleState, Location, MobInstance, Player, Principality, Skill


class MovementError(Exception):
    pass


class BattleError(Exception):
    pass


@dataclass
class GameEngine:
    locations: Dict[str, Location]
    principalities: Dict[str, Principality]

    def move_within_location(self, player: Player, dx: int, dy: int) -> None:
        new_x = player.x + dx
        new_y = player.y + dy
        if not (0 <= new_x <= 15 and 0 <= new_y <= 15):
            raise MovementError("Move stays within 16x16 grid")
        player.x = new_x
        player.y = new_y

    def transition_to_neighbor_location(self, player: Player, target_location: Location) -> None:
        if not self._is_at_edge(player):
            raise MovementError("Transition allowed only at location edge")
        if target_location.location_id == player.current_location_id:
            return
        player.current_location_id = target_location.location_id
        if player.x == 0:
            player.x = 15
        elif player.x == 15:
            player.x = 0
        if player.y == 0:
            player.y = 15
        elif player.y == 15:
            player.y = 0

    def start_battle(
        self,
        battle: Battle,
        attacker: Player,
        defender_hp: int,
        defender_id: str,
        defender_energy_max: int,
    ) -> None:
        """Start battle with full energy for all participants as per contract."""
        battle.state = BattleState.IN_PROGRESS
        battle.start_participant(attacker.player_id, attacker.energy_max, attacker.hp)
        battle.start_participant(defender_id, defender_energy_max, defender_hp)
        battle.turn = 1

    def use_skill(self, battle: Battle, actor_id: str, target_id: str, skill: Skill) -> None:
        if battle.state != BattleState.IN_PROGRESS:
            raise BattleError("Battle not in progress")
        energy = battle.energy_available.get(actor_id, 0)
        if energy < skill.energy_cost:
            raise BattleError("Not enough energy")
        cooldown_key = f"{actor_id}:{skill.name}"
        if battle.cooldowns.get(cooldown_key, 0) > 0:
            raise BattleError("Skill on cooldown")

        # Apply effects
        for effect in skill.effects:
            battle.effects.setdefault(target_id, []).append(effect)

        battle.energy_available[actor_id] = energy - skill.energy_cost
        battle.cooldowns[cooldown_key] = skill.cooldown

    def end_turn(self, battle: Battle) -> None:
        if battle.state != BattleState.IN_PROGRESS:
            raise BattleError("Battle not in progress")
        # decrement cooldowns
        battle.cooldowns = {k: max(0, v - 1) for k, v in battle.cooldowns.items()}
        battle.apply_effects_end_of_turn()
        battle.turn += 1

    def resolve_battle(self, battle: Battle, location: Location, loot_value: int) -> Optional[int]:
        battle.state = BattleState.RESOLVED
        tax_paid = None
        if location.owner_principality_id and location.owner_principality_id in self.principalities:
            tax_pct = 0
            tax_cap = None
            if location.tax_policy:
                tax_pct = location.tax_policy.get("tax_pct", 0)
                tax_cap = location.tax_policy.get("tax_cap")
            tax = int(loot_value * tax_pct / 100)
            if tax_cap is not None:
                tax = min(tax, tax_cap)
            if tax > 0:
                self.principalities[location.owner_principality_id].treasury_value += tax
                tax_paid = tax
        return tax_paid

    def migrate_mob(self, mob: MobInstance, destination: Location, new_x: int, new_y: int) -> None:
        if destination.is_safe_zone:
            raise MovementError("Mobs cannot enter safe zones")
        mob.location_id = destination.location_id
        mob.x = new_x
        mob.y = new_y

    @staticmethod
    def _is_at_edge(player: Player) -> bool:
        return player.x in {0, 15} or player.y in {0, 15}

    def can_take_turn(self, battle: Battle, participant_id: str) -> bool:
        effects = battle.effects.get(participant_id, [])
        if any(e.skip_turn for e in effects):
            return False
        if any(e.fear_chance > 0 for e in effects):
            # TODO: integrate RNG; deterministic skip for now to avoid assumptions
            return False
        return True

