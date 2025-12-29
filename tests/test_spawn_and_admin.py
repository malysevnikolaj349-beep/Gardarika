import os
import hmac
import hashlib
from gardarika.admin import AdminUser, authorize_webapp
from gardarika.loot import split_player_death_loot
from gardarika.models import ItemDefinition, ItemInstance
from gardarika.spawn import SpawnChoice, select_home_city

# Helper to generate valid init_data for tests
def generate_valid_init_data(user_id, token):
    """Generates valid init_data string with hash."""
    data_dict = {
        "auth_date": "1620000000",
        "query_id": "AABBCCDD",
        "user": f'{{"id":{user_id},"first_name":"Test","last_name":"User","username":"testuser"}}'
    }
    sorted_keys = sorted(data_dict.keys())
    data_check_string = "\n".join([f"{k}={data_dict[k]}" for k in sorted_keys])
    secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    hash_val = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    data_dict["hash"] = hash_val
    return data_dict

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
    token = "test_token"
    os.environ["TELEGRAM_TOKEN"] = token
    admin_users = {1: AdminUser(tg_id=1, role_id="owner", is_active=True)}

    try:
        authorize_webapp(None, admin_users)
    except PermissionError:
        pass
    else:
        raise AssertionError("initData must be required")

    # Generate valid data for the active admin test
    valid_data = generate_valid_init_data(1, token)
    active_admin = authorize_webapp(valid_data, admin_users)
    assert active_admin.tg_id == 1

    inactive_users = {1: AdminUser(tg_id=1, role_id="owner", is_active=False)}

    # Even with valid signature, inactive admin should be blocked
    try:
        authorize_webapp(valid_data, inactive_users)
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
