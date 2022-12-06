import asyncio
import random

import discord
from discord.ext import commands

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.loop.create_task(self.change_bot_presence())

    async def change_bot_presence(self):
        await self.bot.wait_until_ready()

        servers = "server" if len(self.bot.guilds) == 1 else "servers"
        gremlins = "gremlin" if len(self.bot.users) == 1 else "gremlins"

        status = {
            1: {
                "Activity": discord.ActivityType.watching,
                "Status": ["cat videos", f"{len(self.bot.users)} {gremlins} in {len(self.bot.guilds)} {servers}", "Jerma compilations", "the demons in my puter"],
            },
            2: {
                "Activity": discord.ActivityType.playing,
                "Status": ["with cats", "Madden NFL 06 on XBOX", "with lasers"],
            },
            3: {
                "Activity": discord.ActivityType.listening,
                "Status": ["the screams of the damned", f"cat activation noise compilation #{random.randint(1, 1000)}"],
            },
        }

        index = random.randint(1, 3)
        activity = status[index]["Activity"]
        string = random.choice(status[index]["Status"])

        while not self.bot.is_closed():
            await self.bot.change_presence(activity=discord.Activity(type=activity, name=string))
            await asyncio.sleep(60 * 5)  # 5 minutes

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Activity(bot))
