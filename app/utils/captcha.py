from typing import Optional

import aiohttp

from app.utils.config import config

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
TIMEOUT = 5


async def verify_recaptcha(
        token: str,
        remote_ip: Optional[str] = None,
        action: Optional[str] = None
) -> bool:
    if not token:
        raise ValueError("reCAPTCHA token is required")
    try:
        payload = {
            "secret": config.recaptcha_secret_key,
            "response": token,
        }
        if remote_ip:
            payload["remoteip"] = remote_ip
        async with aiohttp.ClientSession() as session:
            async with session.post(RECAPTCHA_VERIFY_URL, data=payload) as resp:
                result = await resp.json()
                if not result.get("success"):
                    return False
                if "score" in result:
                    return result["score"] >= config.recaptcha_threshold
                return True
    except Exception as e:
        return False
