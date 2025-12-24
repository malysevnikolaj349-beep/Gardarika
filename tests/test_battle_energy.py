from gardarika.game_engine import BattleError, GameEngine
from gardarika.models import Battle, BattleEffect, BattleState, Location, MobInstance, Player, Principality, Skill


def build_engine():
    loc = Location(
        location_id="loc-1",
        world_x=0,
        world_y=0,
        biome="plains",
        owner_principality_id=None,
        is_safe_zone=False,
    )
    return GameEngine(locations={loc.location_id: loc}, principalities={})


def test_energy_full_on_start_and_not_regen():
    engine = build_engine()
    player = Player(
        tg_id=1,
        player_id="p1",
        home_city_id="c1",
        current_location_id="loc-1",
        x=0,
        y=0,
        hp=100,
        hp_max=100,
        level=1,
        xp=0,
        fame=0,
        fear=0,
        energy_max=5,
    )
    battle = Battle(
        battle_id="b1",
        location_id="loc-1",
        x=0,
        y=0,
        battle_type="pve",
        turn=0,
        state=BattleState.PREPARING,
    )
    engine.start_battle(battle, player, defender_hp=20, defender_id="mob1", defender_energy_max=5)
    assert battle.energy_available[player.player_id] == 5

    skill = Skill(name="slash", energy_cost=3, cooldown=1)
    engine.use_skill(battle, player.player_id, "mob1", skill)
    assert battle.energy_available[player.player_id] == 2

    engine.end_turn(battle)
    assert battle.energy_available[player.player_id] == 2


def test_skill_respects_cooldown():
    engine = build_engine()
    player = Player(
        tg_id=1,
        player_id="p1",
        home_city_id="c1",
        current_location_id="loc-1",
        x=0,
        y=0,
        hp=100,
        hp_max=100,
        level=1,
        xp=0,
        fame=0,
        fear=0,
        energy_max=10,
    )
    battle = Battle(
        battle_id="b1",
        location_id="loc-1",
        x=0,
        y=0,
        battle_type="pve",
        turn=0,
        state=BattleState.PREPARING,
    )
    engine.start_battle(battle, player, defender_hp=20, defender_id="mob1", defender_energy_max=10)
    skill = Skill(name="stun", energy_cost=2, cooldown=2, effects=[BattleEffect("stun", 2, skip_turn=True)])
    engine.use_skill(battle, player.player_id, "mob1", skill)
    try:
        engine.use_skill(battle, player.player_id, "mob1", skill)
    except BattleError:
        pass
    else:
        raise AssertionError("Skill should be on cooldown")


def test_bleed_and_skip_turn_effects():
    engine = build_engine()
    battle = Battle(
        battle_id="b1",
        location_id="loc-1",
        x=0,
        y=0,
        battle_type="pve",
        turn=0,
        state=BattleState.IN_PROGRESS,
    )
    battle.start_participant("p1", energy_max=10, hp=30)
    bleed = BattleEffect(name="bleed", remaining_turns=2, bleed_damage=5)
    skip = BattleEffect(name="stun", remaining_turns=1, skip_turn=True)
    battle.effects["p1"] = [bleed, skip]

    assert not engine.can_take_turn(battle, "p1")
    engine.end_turn(battle)
    assert battle.participants_hp["p1"] == 25
    assert engine.can_take_turn(battle, "p1")

    engine.end_turn(battle)
    assert battle.participants_hp["p1"] == 20
    assert engine.can_take_turn(battle, "p1")


def test_persistent_mob_hp_and_safe_zone_migration_blocked():
    city_location = Location(
        location_id="city",
        world_x=0,
        world_y=1,
        biome="city",
        owner_principality_id=None,
        is_safe_zone=True,
    )
    field_location = Location(
        location_id="field",
        world_x=0,
        world_y=0,
        biome="field",
        owner_principality_id=None,
        is_safe_zone=False,
    )
    engine = GameEngine(locations={"city": city_location, "field": field_location}, principalities={})
    mob = MobInstance(
        mob_instance_id="m1",
        mob_def_id="wolf",
        unique_name=None,
        location_id="field",
        x=5,
        y=5,
        hp_current=20,
        level_current=1,
    )
    mob.hp_current = 4
    try:
        engine.migrate_mob(mob, city_location, 0, 0)
    except Exception:
        pass
    else:
        raise AssertionError("Mob should not enter safe zone")

    engine.migrate_mob(mob, field_location, 1, 1)
    assert mob.hp_current == 4  # unchanged across migrations/battles


def test_transition_requires_edge():
    engine = build_engine()
    neighbor = Location(
        location_id="loc-2",
        world_x=1,
        world_y=0,
        biome="plains",
        owner_principality_id=None,
        is_safe_zone=False,
    )
    engine.locations[neighbor.location_id] = neighbor
    player = Player(
        tg_id=1,
        player_id="p1",
        home_city_id="c1",
        current_location_id="loc-1",
        x=5,
        y=5,
        hp=100,
        hp_max=100,
        level=1,
        xp=0,
        fame=0,
        fear=0,
        energy_max=10,
    )
    target = neighbor
    try:
        engine.transition_to_neighbor_location(player, target)
    except Exception:
        pass
    else:
        raise AssertionError("Transition should fail away from edge")

    player.x = 15
    engine.transition_to_neighbor_location(player, target)
    assert player.x == 0


def test_tax_capped_and_deposited():
    principality = Principality(principality_id="pr1", name="North")
    taxed_location = Location(
        location_id="loc-2",
        world_x=0,
        world_y=0,
        biome="plains",
        owner_principality_id=principality.principality_id,
        is_safe_zone=False,
        tax_policy={"tax_pct": 20, "tax_cap": 10},
    )
    engine = GameEngine(locations={taxed_location.location_id: taxed_location}, principalities={principality.principality_id: principality})
    battle = Battle(
        battle_id="b2",
        location_id=taxed_location.location_id,
        x=0,
        y=0,
        battle_type="pve",
        turn=0,
        state=BattleState.IN_PROGRESS,
    )
    tax = engine.resolve_battle(battle, taxed_location, loot_value=200)
    assert tax == 10
    assert principality.treasury_value == 10

