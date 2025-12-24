from gardarika.admin import AdminUser, authorize_webapp
from gardarika.loot import split_player_death_loot
from gardarika.models import ItemDefinition, ItemInstance
from gardarika.spawn import SpawnChoice, select_home_city


def test_home_city_selection_respects_spawn_enabled():
    cities = [
        SpawnChoice(city_id="c1", name="Novice", spawn_enabled=False, spawn_capacity=100, population={}),
        SpawnChoice(city_id="c2", name="OpenCity", spawn_enabled=True, spawn_capacity=5, population={}),
    ]
    home_city = select_home_city(cities, fallback_city_id="c1")
    assert home_city == "c2"

    cities[1].spawn_enabled = False
    home_city = select_home_city(cities, fallback_city_id="c1")
    assert home_city == "c1"


def test_admin_requires_initdata_and_active_flag():
    admin_users = {1: AdminUser(tg_id=1, role_id="owner", is_active=True)}

    try:
        authorize_webapp(None, admin_users)
    except PermissionError:
        pass
    else:
        raise AssertionError("initData must be required")

    active_admin = authorize_webapp({"tg_id": "1"}, admin_users)
    assert active_admin.tg_id == 1

    inactive_users = {1: AdminUser(tg_id=1, role_id="owner", is_active=False)}
    try:
        authorize_webapp({"tg_id": "1"}, inactive_users)
    except PermissionError:
        pass
    else:
        raise AssertionError("inactive admin should be blocked")


def test_loot_visibility_split():
    def mk_item(idx: int) -> ItemInstance:
        return ItemInstance(ItemDefinition(item_def_id=f"i{idx}", name=f"Item {idx}", base_value=10), instance_id=f"ins{idx}")

    loot = [mk_item(1), mk_item(2), mk_item(3)]
    split = split_player_death_loot("loc", 0, 0, loot)

    assert len(split.killer_visible) == 1
    assert split.ground_pile.items  # public pile exists
    assert len(split.hidden) == 1

