from app.utils.config import config
import aiohttp

RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


async def verify_recaptcha(token: str) -> bool:
    """Проверяет токен reCAPTCHA через Google API"""
    async with aiohttp.AsyncClient() as client:
        response = await client.post(
            RECAPTCHA_VERIFY_URL,
            data={"secret": config.recaptcha_secret_key, "response": token},
        )
        result = response.json()
        return result.get("success", False)
