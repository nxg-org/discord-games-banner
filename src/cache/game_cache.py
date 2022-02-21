
from __future__ import annotations
import time
from typing import TYPE_CHECKING, Any, Optional
from discord import MemberCacheFlags
if TYPE_CHECKING:
    from bot.my_client import MyClient

from datetime import datetime
import nextcord
import json

from lib.util import cache_dump_default


class GameCache:

    def __init__(self, bot: MyClient):
        self.bot = bot
        self.cache = {
            "blacklist": {
                "Genshin Impact": 3600
            },
            "whitelist_members": set(),
            "watchlist": {

            }
        }

    def add_game_to_blacklist(self, game_name: str, time_period: int = 3600) -> None:
        self.cache["blacklist"][game_name] = time_period

    def update_blacklist_game(self, game_name: str, time_period: int) -> None:
        self.cache["blacklist"][game_name] = time_period

    def remove_game_from_blacklist(self, game_name: str) -> None:
        del self.cache["blacklist"][game_name]

    def game_in_blacklist(self, game_name: str | None) -> bool:
        return game_name in self.cache["blacklist"]

    def format_blacklist(self) -> str:
        tmp: dict[str, int] = self.cache["blacklist"]
        return ' '.join(f"{item[0]}: {item[1]}" for item in tmp.items())

    def add_member_to_whitelist(self, member_id: int) -> None:
        self.cache["whitelist_members"].add(member_id)
        del self.cache["watchlist"][member_id]

    def remove_member_from_whitelist(self, member_id: int) -> None:
        self.cache["whitelist_members"].remove(member_id)

    def member_in_whitelist(self, member_id: int) -> None:
        return member_id in self.cache["whitelist_members"]

    def should_add_member_to_watchlist(self, member: nextcord.Member) -> bool:
        return bool(next((game.name for game in member.activities if self.game_in_blacklist(game.name)), None))

    def add_member_to_watchlist(self, member_id: int, time_playing: Optional[int] = None) -> None:
        if member_id in self.cache["watchlist"]:
            return
        if member_id in self.cache["whitelist_members"]:
            return
        if not time_playing:
            time_playing = time.time()
        self.cache["watchlist"][member_id] = time_playing

    def update_watchlist_member(self, member_id: int, time_playing: int) -> None:
        self.cache["watchlist"][member_id] = time_playing

    def remove_member_from_watchlist(self, member_id: int) -> None:
        del self.cache["watchlist"][member_id]

    def get_start_time(self, member_id: int) -> int:
        return self.cache["watchlist"][member_id]

    def member_in_watchlist(self, member_id: int) -> bool:
        return member_id in self.cache["watchlist"]

    def time_differential(self, member_id: int, time_played: int) -> bool:
        if member_id not in self.cache["watchlist"]:
            return 0
        return time_played - self.cache["watchlist"][member_id]

    def is_time_bad(self, game_name: str, member_id: int) -> bool:
        time_start = self.cache["watchlist"].get(member_id)
        if not time_start:
            self.add_member_to_watchlist(member_id)
            return False
        return time.time() - time_start >= self.cache["blacklist"][game_name]

    def dump_cache_to_file(self):
        with open('lib/cache/storage/data.json', 'w') as outfile:
            json.dump(self.cache, outfile, default=cache_dump_default)

    def load_cache_from_file(self, filename: Optional[str]):
        if not filename:
            filename = 'lib/cache/storage/data.json'
        with open(filename, 'r') as outfile:
            self.cache = json.load(outfile)
            self.cache["whitelist_members"] = set(
                self.cache["whitelist_members"])
