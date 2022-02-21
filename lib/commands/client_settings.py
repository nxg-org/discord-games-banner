
from __future__ import annotations
from typing import TYPE_CHECKING
from discord import MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient


import nextcord


async def change_presence(bot: MyClient, message: nextcord.Message) -> None:
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Activity(name="fuck", type=nextcord.ActivityType.custom, state="shit"))


async def check_loops(bot: MyClient, message: nextcord.Message) -> None:
    for loop in bot.loops.items():
        print(loop)