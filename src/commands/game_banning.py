
from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from bot.my_client import MyClient
    from cache.game_cache import GameCache
import nextcord
import time


async def add_game(bot: MyClient, message: nextcord.Message) -> None:
    split = message.clean_content.split(' ')
    if len(split) >= 3:
        wanted_time = int(split[1])
        wanted_game = ' '.join(split[2:])
        bot.cache.add_game_to_blacklist(wanted_game, wanted_time)
        await message.channel.send("added \"" + wanted_game + "\".")



async def remove_game(bot: MyClient, message: nextcord.Message) -> None:
    split = message.clean_content.split(' ')
    if len(split) > 1:
        wanted_game = ' '.join(split[1:])
        bot.cache.remove_game_from_blacklist(wanted_game)
        await message.channel.send("removed \"" + wanted_game + "\".")





async def check_for_banned_games(bot: MyClient, message: nextcord.Message) -> None:
    wanted_id = int(message.clean_content.split(' ')[1])
    guild = nextcord.utils.find(lambda g: g.id == wanted_id, bot.guilds)
    bad_members = await search_guild(guild, bot.cache, False)

    bad_members_message = []
    current_time = time.time()
    for member in bad_members:
        bad_members_message.append(member.name + ": bad for " + str(
            round(bot.cache.time_differential(member.id, current_time))) + " seconds.")

    await message.channel.send('Bad members:\n' + '\n'.join(bad_members_message))


async def search_guild(guild: nextcord.Guild, cache: GameCache, need_time: bool = True) -> list[nextcord.Member]:
    all_member_ids = guild.fetch_members(limit=None).map(lambda m: m.id).chunk(100)
    all_members = []
    async for mem_chunk in all_member_ids:
        all_members.append(await guild.query_members(user_ids=mem_chunk, limit=100, presences=True, cache=True))

    # flattening list.
    flat_members: list[nextcord.Member] = [
        item for mem_chunk in all_members for item in mem_chunk]

    bad_members = []
    for member in flat_members:
        bad_game = next((game.name for game in member.activities if cache.game_in_blacklist(game.name)), None)
        if bad_game and not cache.member_in_whitelist(member.id):
            cache.add_member_to_watchlist(member.id)
            if not need_time or cache.is_time_bad(bad_game, member.id):
                bad_members.append(member)
    return bad_members
    # bad_members.append(member.name + ": bad for " + str(round(cache.time_differential(member.id, time.time()))) + " seconds.")
