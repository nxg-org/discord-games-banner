

import asyncio
from typing import Optional
import nextcord

from src.cache import GameCache
import src.commands
import src.loops


class MyClient(nextcord.Client):


    def __init__(self, prefix: str, owner_id: Optional[int] = None, auto_ban: bool = False, loop: Optional[asyncio.AbstractEventLoop] = None, **kwargs):
        super().__init__(loop=loop, **kwargs)
        self.prefix = prefix
        self.cmds = {}
        self.loops = {}
        self.cache = GameCache(self)
        self.auto_ban = auto_ban
        self.loop.create_task(self.custom_ready_wait())
        self.owner = None
        self.owner_id = owner_id
        for item in src.commands.__dict__.items():
            if callable(item[1]):
                print(item)
                self.cmds[item[0]] = item[1]

        

                

    async def custom_ready_wait(self):
        await self.wait_until_ready()
        self.owner = await self.fetch_user(self.owner_id) if self.owner_id else (await self.application_info()).owner
        self.owner_id = self.owner.id

        for item in src.loops.__dict__.items():
            if (callable(item[1])):
                print(item)
                self.loops[item[0]] = self.loop.create_task(item[1](self))


    async def on_message(self, message: nextcord.Message) -> None:
        split = message.clean_content.split(' ')
        clean_split = split[0].removeprefix(self.prefix)
        if (message.author.id != self.user.id and clean_split != split[0]):
            try:
                await (self.cmds.get(clean_split, self.on_command_error))(self, message)
            except TypeError as e:
                print(e.with_traceback(None)) # command not found.
            except Exception as e:
                print(e.with_traceback(None))


    async def on_presence_update(self, before: nextcord.Member, after: nextcord.Member):
        if self.cache.should_add_member_to_watchlist(after):
            self.cache.add_member_to_watchlist(after.id)
        elif self.cache.member_in_watchlist(after.id):
            self.cache.remove_member_from_watchlist(after.id)

    
    async def on_command_error(self, selfAgain, message: nextcord.Message) -> None:
        await message.delete()
        await message.channel.send("Fucked up command. Good job, retard.")

    

