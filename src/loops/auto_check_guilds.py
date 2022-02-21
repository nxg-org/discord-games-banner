from __future__ import annotations
import asyncio
import time
from typing import TYPE_CHECKING
from discord import DMChannel, MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient


import nextcord
from src.commands.game_banning import search_guild


async def check_all_guilds(bot: MyClient) -> None:
    while True:
        start = time.time()
        for completed in asyncio.as_completed(fs=[search_guild(guild, bot.cache) for guild in bot.guilds]):
            results: list[nextcord.Member] = await completed
        
            if len(results) > 0:
                guild = results[0].guild
                if not bot.auto_ban:
                    await bot.owner.send(f'Checking for: {bot.cache.format_blacklist()}\nGuild: {guild}\n   - ' + '\n  - '.join(list(map(lambda m: f"{m.name}: Bad for {round(bot.cache.time_differential(m.id, time.time()))} seconds.", results))))
                else:
                    await bot.owner.send(f'Checking for: {bot.cache.format_blacklist()}\nGuild: {guild}\n   - ' + '\n  - [BANNED] '.join([m.name for m in results]), results)
                    for member in results:
                        await member.ban(delete_message_days=0, reason="You were playing a shitty game for too long, lol.")

        offset = 60 - time.time() - start
        await asyncio.sleep(60 if offset < 0 else offset)
