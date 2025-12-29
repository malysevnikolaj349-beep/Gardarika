from __future__ import annotations

import os
import hmac
import hashlib
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Role:
    role_id: str
    name: str
    permissions: List[str]


@dataclass
class AdminUser:
    tg_id: int
    role_id: str
    is_active: bool
    last_login_at: Optional[str] = None


@dataclass
class AdminAuditLog:
    actor_tg_id: int
    as_tg_id: int
    action: str
    target: str
    before_json: str
    after_json: str
    reason: str
    created_at: str


def authorize_webapp(init_data: Optional[Dict[str, str]], admin_users: Dict[int, AdminUser]) -> AdminUser:
    """Validate Telegram WebApp initData before granting access.

    Verifies the cryptographic signature of the initData using the bot token.
    """
    if not init_data:
        raise PermissionError("Telegram WebApp initData required")

    hash_val = init_data.get("hash")
    if not hash_val:
        raise PermissionError("hash missing in initData")

    # 1. Construct the data-check-string
    # The keys are sorted alphabetically.
    # NOTE: 'hash' is excluded from the data-check-string.
    # The 'tg_id' field in init_data seems to be a convenience field added by the frontend wrapper?
    # Standard Telegram initData contains: query_id, user, auth_date, hash.
    # 'user' is a JSON string.
    # We should verify the hash against the rest of the fields.

    data_check_arr = []
    for key, value in sorted(init_data.items()):
        if key != "hash" and key != "tg_id": # tg_id might be extra field, check if it's part of signed data
             data_check_arr.append(f"{key}={value}")

    # If tg_id is not part of standard initData (it's inside 'user' JSON), we shouldn't include it in check string
    # unless it was passed as a top level param in the URL query string from Telegram.
    # Assuming init_data is the parsed query string parameters.

    data_check_string = "\n".join(data_check_arr)

    # 2. Calculate the secret key
    # Ensure os is imported (it is at the top of the file, but let's be sure it's accessible here)
    bot_token = os.getenv("TELEGRAM_TOKEN")
    if not bot_token:
        raise RuntimeError("TELEGRAM_TOKEN not set")

    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()

    # 3. Calculate the hash
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # 4. Compare
    if calculated_hash != hash_val:
        raise PermissionError("invalid initData signature")

    # 5. Extract User ID and check admin
    # 'user' field is a JSON string
    import json
    try:
        user_data = json.loads(init_data.get("user", "{}"))
        tg_id = user_data.get("id")
        if not tg_id:
             # Fallback if tg_id was passed separately (non-standard but possible in internal passing)
             tg_id = int(init_data.get("tg_id", 0))
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise PermissionError("invalid user data") from exc

    admin = admin_users.get(tg_id)
    if not admin or not admin.is_active:
        raise PermissionError("admin access denied")

    return admin
