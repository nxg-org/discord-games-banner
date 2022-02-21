from __future__ import annotations
from typing import TYPE_CHECKING
from discord import MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient


import nextcord


async def load_cache(bot: MyClient, message: nextcord.Message):
    split = message.clean_content.split(' ')
    if len(split) == 2:
        filename = split[1]
    else:
        filename = None
    bot.cache.load_cache_from_file(filename)


async def dump_cache(bot: MyClient, message: nextcord.Message):
    bot.cache.dump_cache_to_file()
