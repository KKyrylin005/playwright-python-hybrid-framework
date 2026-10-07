"""SauceDemo has no backend: auth is a cookie and the cart lives in localStorage.

Building a Playwright ``storage_state`` lets a test start already logged in, with a
pre-filled cart, skipping the UI steps that other tests already cover.
"""

import json
from collections.abc import Iterable
from typing import Any
from urllib.parse import urlparse

SESSION_COOKIE = "session-username"
CART_STORAGE_KEY = "cart-contents"


def build_storage_state(
    base_url: str, username: str, cart_product_ids: Iterable[int] = ()
) -> dict[str, Any]:
    cart = list(cart_product_ids)
    session_cookie = {
        "name": SESSION_COOKIE,
        "value": username,
        "domain": urlparse(base_url).hostname,
        "path": "/",
        "expires": -1,
        "httpOnly": False,
        "secure": False,
        "sameSite": "Lax",
    }
    local_storage = [{"name": CART_STORAGE_KEY, "value": json.dumps(cart)}] if cart else []
    return {
        "cookies": [session_cookie],
        "origins": [{"origin": base_url, "localStorage": local_storage}],
    }
