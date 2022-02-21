from __future__ import annotations
from typing import TYPE_CHECKING
from discord import MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient


import nextcord


async def whitelist_member(bot: MyClient, message: nextcord.Message) -> None:
    split = message.clean_content.split(' ')
    if len(split) == 1:
        await message.channel.send("No ID specified.")
    else:
        bot.cache.add_member_to_whitelist(int(split[1]))


async def remove_whitelist(bot: MyClient, message: nextcord.Message) -> None:
    split = message.clean_content.split(' ')
    if len(split) == 1:
        await message.channel.send("No ID specified.")
    else:
        bot.cache.remove_member_from_whitelist(int(split[1]))
