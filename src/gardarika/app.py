"""
Command-line demo entrypoint for the Gardarika domain scaffold.

This intentionally minimal CLI walks through a deterministic scenario that
honors the implementation contract: movement is constrained to 16x16 tiles,
transitions happen only on edges, battles always start with full energy and
respect cooldown/energy costs, mobs cannot enter safe zones, and taxes are
routed to owning principalities. The output is purely textual so the demo can
run in environments without Telegram/WebApp integration.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from typing import Dict, List

from .game_engine import BattleError, GameEngine, MovementError
from .models import (
    Battle,
    BattleEffect,
    BattleState,
    City,
    Location,
    MobInstance,
    Player,
    Principality,
    Skill,
)


@dataclass
class DemoWorld:
    engine: GameEngine
    locations: Dict[str, Location]
    principalities: Dict[str, Principality]
    cities: Dict[str, City]
    player: Player
    mobs: List[MobInstance] = field(default_factory=list)

    def mobs_in_location(self, location_id: str) -> List[MobInstance]:
        return [m for m in self.mobs if m.location_id == location_id]


def build_demo_world() -> DemoWorld:
    north_realm = Principality(principality_id="principality-north", name="Северные земли")
    origin = Location(
        location_id="origin-plain",
        world_x=0,
        world_y=0,
        biome="plains",
        owner_principality_id=None,
        is_safe_zone=False,
        tax_policy=None,
    )
    east = Location(
        location_id="east-province",
        world_x=1,
        world_y=0,
        biome="forest",
        owner_principality_id=north_realm.principality_id,
        is_safe_zone=False,
        tax_policy={"tax_pct": 10, "tax_cap": 5},
    )
    cities = {
        "starter-town": City(
            city_id="starter-town",
            name="Город новичков",
            location_id=origin.location_id,
            owner_principality_id=None,
            state="prosper",
            spawn_enabled=True,
            spawn_capacity=10,
        )
    }
    principalities = {north_realm.principality_id: north_realm}
    engine = GameEngine(locations={origin.location_id: origin, east.location_id: east}, principalities=principalities)
    player = Player(
        tg_id=1001,
        player_id="player-1",
        home_city_id=cities["starter-town"].city_id,
        current_location_id=origin.location_id,
        x=8,
        y=8,
        hp=30,
        hp_max=30,
        level=1,
        xp=0,
        fame=0,
        fear=0,
    )
    mobs = [
        MobInstance(
            mob_instance_id="wolf-1",
            mob_def_id="wolf",
            unique_name=None,
            location_id=east.location_id,
            x=5,
            y=5,
            hp_current=24,
            level_current=2,
        )
    ]
    return DemoWorld(engine=engine, locations=engine.locations, principalities=principalities, cities=cities, player=player, mobs=mobs)


def render_location(world: DemoWorld) -> str:
    grid = [["." for _ in range(16)] for _ in range(16)]
    player = world.player
    if player.current_location_id in world.locations:
        grid[player.y][player.x] = "P"
    for mob in world.mobs_in_location(player.current_location_id):
        grid[mob.y][mob.x] = "M" if not mob.is_boss else "B"
    rendered_rows = ["".join(row) for row in grid]
    return "\n".join(rendered_rows)


def perform_demo_steps(world: DemoWorld) -> None:
    print("Gardarika Demo: constrained map, battle, and tax flow\n")
    print("Initial location: origin-plain (0,0). Player starts at (8,8).")
    print(render_location(world))
    print("\nAttempting an out-of-bounds move to demonstrate 16x16 guard...")
    try:
        world.engine.move_within_location(world.player, dx=10, dy=0)
    except MovementError as exc:
        print(f"Blocked: {exc}")

    print("\nMarching east to the edge (x=15) within the origin location...")
    while world.player.x < 15:
        world.engine.move_within_location(world.player, dx=1, dy=0)
    print(f"Player is now at edge ({world.player.x},{world.player.y}).")

    print("Transitioning to neighboring east-province across the edge...")
    world.engine.transition_to_neighbor_location(world.player, world.locations["east-province"])
    print(f"New location: {world.player.current_location_id} at ({world.player.x},{world.player.y}).")

    mob = world.mobs[0]
    print("\nEncountering a roaming mob; its HP persists between battles.")
    battle = Battle(
        battle_id="battle-1",
        location_id=world.player.current_location_id,
        x=mob.x,
        y=mob.y,
        battle_type="pve",
        turn=0,
        state=BattleState.PREPARING,
    )
    world.engine.start_battle(battle, attacker=world.player, defender_hp=mob.hp_current, defender_id=mob.mob_instance_id, defender_energy_max=10)
    print(f"Battle started: attacker energy={battle.energy_available[world.player.player_id]}, defender HP={battle.participants_hp[mob.mob_instance_id]}")

    strike = Skill(
        name="strike",
        energy_cost=3,
        cooldown=1,
        effects=[BattleEffect(name="bleed", remaining_turns=2, bleed_damage=2)],
    )
    print("Using a skill that applies bleed and consumes energy...")
    world.engine.use_skill(battle, actor_id=world.player.player_id, target_id=mob.mob_instance_id, skill=strike)
    print(f"Energy after strike: {battle.energy_available[world.player.player_id]}; cooldown set to {battle.cooldowns}")

    print("Ending turn to tick cooldowns and bleed effects...")
    world.engine.end_turn(battle)
    print(f"Turn {battle.turn}: defender HP now {battle.participants_hp[mob.mob_instance_id]} (bleed applied).")

    print("Resolving battle and sending tax to the province owner (10% capped at 5)...")
    tax_paid = world.engine.resolve_battle(battle, location=world.locations[world.player.current_location_id], loot_value=50)
    print(f"Tax routed to principality treasury: {tax_paid}; current treasury={world.principalities['principality-north'].treasury_value}")
    print("\nDemo complete. All actions respected the movement, battle, and tax contract invariants.")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a deterministic Gardarika domain demo.")
    subparsers = parser.add_subparsers(dest="command", required=False)
    subparsers.add_parser("demo", help="Run the built-in contract demo (default).")
    subparsers.add_parser("render", help="Render the starting 16x16 map and exit.")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    world = build_demo_world()

    if args.command == "render":
        print(render_location(world))
        return

    # Default to demo when no subcommand specified
    perform_demo_steps(world)


if __name__ == "__main__":
    main()
