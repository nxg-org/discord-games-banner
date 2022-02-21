from __future__ import annotations
from typing import TYPE_CHECKING
from discord import MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient


import nextcord
from .. import commands

async def help(bot: MyClient, message: nextcord.Message) -> None:
    msg = '\n'.join([item[0] for item in commands.__dict__.items() if not item[0].startswith("__") and callable(item[1])])
    await message.channel.send(msg)
