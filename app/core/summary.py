import aiohttp

from app.utils.config import config

HEADERS = {'Authorization': f'Bearer {config.yandex_api_token}'}


async def summarize_request(session, headers, url, data):
    async with session.post(url=url, headers=headers, data=data) as response:
        return await response.text()


async def summary():
    async with aiohttp.ClientSession() as session:
        ...
        # response = summarize_request(session, config.yandex_api_url)
        # print(response)
