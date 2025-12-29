from __future__ import annotations

import hashlib
import hmac
import json
import os
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

    Verifies the HMAC signature of the initData using TELEGRAM_TOKEN.
    Extracts the user ID from the 'user' JSON object or 'tg_id' field.

    Raises:
        PermissionError: If validation fails or admin access is denied.
        EnvironmentError: If TELEGRAM_TOKEN is not set.
    """

    if not init_data:
        raise PermissionError("Telegram WebApp initData required")

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise EnvironmentError("TELEGRAM_TOKEN environment variable not set")

    # Verify HMAC signature
    received_hash = init_data.get("hash")
    if not received_hash:
        raise PermissionError("hash missing in initData")

    data_check_arr = []
    # Sort keys to ensure consistent order for HMAC calculation
    for key in sorted(init_data.keys()):
        if key != "hash":
            data_check_arr.append(f"{key}={init_data[key]}")
    data_check_string = "\n".join(data_check_arr)

    secret_key = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if computed_hash != received_hash:
        raise PermissionError("initData signature mismatch")

    # Extract tg_id
    tg_id_raw = None

    # Try extracting from 'user' field (preferred)
    user_json = init_data.get("user")
    if user_json:
        try:
            user_data = json.loads(user_json)
            tg_id_raw = user_data.get("id")
        except json.JSONDecodeError:
            pass

    # Fallback to 'tg_id' field
    if tg_id_raw is None:
        tg_id_raw = init_data.get("tg_id")

    if tg_id_raw is None:
        raise PermissionError("tg_id missing in initData")

    try:
        tg_id = int(tg_id_raw)
    except ValueError as exc:
        raise PermissionError("invalid tg_id") from exc

    admin = admin_users.get(tg_id)
    if not admin or not admin.is_active:
        raise PermissionError("admin access denied")

    return admin
