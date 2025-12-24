from __future__ import annotations

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

    The full signature verification is out of scope here; the function enforces that
    init_data is present (per contract 3.9/4.H.20) and that the tg_id belongs to an
    active admin. A TODO is left for the cryptographic check to avoid inventing
    protocol details.
    """

    if not init_data:
        raise PermissionError("Telegram WebApp initData required")

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

    # TODO: verify initData HMAC signature per Telegram spec.
    return admin

