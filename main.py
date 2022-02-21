# /usr/bin/python3.10
import nextcord
from src.bot import MyClient
from config import *





def main():
    bot = MyClient(owner_id=config.owner_id, prefix=config.prefix, auto_ban=config.auto_ban, intents=nextcord.Intents.all())
    bot.run(config.token)




if __name__ == "__main__":
    main()
