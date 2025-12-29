from unittest.mock import patch
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

    # The authorize_webapp function now requires TELEGRAM_TOKEN and valid hash.
    # For this test, we mock TELEGRAM_TOKEN and ignore the hash check by patching os.getenv
    # OR we must provide a valid hash.
    # Since this test focuses on "active flag" and "tg_id", not the signature verification itself
    # (which is tested in test_admin_auth.py), it's easier to mock the verification bypass
    # OR mock the token AND provide a matching signature.

    # However, since authorize_webapp is now strict, we can't just pass {"tg_id": "1"} if token is present.
    # And if token is NOT present, it raises EnvironmentError.

    # So we MUST patch os.getenv to return a token, AND compute the signature.
    # OR, we can patch `gardarika.admin.hmac` to bypass verification?
    # Or patch `gardarika.admin.authorize_webapp`? No, we are testing it.

    # Let's generate a valid signature using a dummy token.
    token = "dummy_token"

    import hmac
    import hashlib

    def sign(data):
        # We only have tg_id=1
        data_check_string = "tg_id=1"
        secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
        return hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    init_data = {"tg_id": "1"}
    init_data["hash"] = sign(init_data)

    with patch("os.getenv", return_value=token):
        active_admin = authorize_webapp(init_data, admin_users)
        assert active_admin.tg_id == 1

        inactive_users = {1: AdminUser(tg_id=1, role_id="owner", is_active=False)}
        try:
            authorize_webapp(init_data, inactive_users)
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
