from dataclasses import dataclass
from datetime import datetime
from typing import List

from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from app.utils.config import config


@dataclass
class Post:
    text: str
    channel_link: str
    date: datetime


def create_client(session_name: str) -> TelegramClient:
    return TelegramClient(session_name, config.telegram_account_api_id, config.telegram_api_hash)


async def fetch_channel_history(client: TelegramClient, channel_username: str, target: str, count: int) -> List[Post]:
    entity = await client.get_entity(channel_username)
    posts = []
    offset_id = 0

    while len(posts) < count:
        history = await client(GetHistoryRequest(
            peer=entity,
            limit=min(100, count - len(posts)),
            offset_date=None,
            offset_id=offset_id,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        if not history.messages:
            break

        for msg in history.messages:
            offset_id = msg.id
            if not target or (msg.message and target.lower() in msg.message.lower()):
                post = Post(
                    text=msg.message,
                    channel_link=f"https://t.me/{channel_username}/{msg.id}",
                    date=msg.date
                )
                posts.append(post)

                if len(posts) >= count:
                    break

    return posts


async def display_posts(client: TelegramClient, channel_username: str, target: str, count: int):
    posts = await fetch_channel_history(client, channel_username, target, count)
    for p in posts:
        print(f"дата: {p.date} \n {p.text} \n ссылка: {p.channel_link}\n")

# async def main():
#     async with create_client("session_name") as client:
#         await display_posts(client, channel_username=CHANNELS_FOR_PARSING[1], target="газ", count=10)
