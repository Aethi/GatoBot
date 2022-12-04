# GatoBot - couldntbe.me

# Discord imports
import discord
from discord.ext import commands

# Our imports
from strformat import StrFmt

# Standard imports
import requests
import logging
import json

# Use Discord.py's prewritten logger format
discord.utils.setup_logging()

class GatoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='hey gato, ', # Unused
            intents=discord.Intents.all()
        )

        self.initial_extensions = [
            'cogs.admin',
            'cogs.chat',
            'cogs.rpc',
            'cogs.fun'
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await self.tree.sync()

    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info(f"Discord.py version: {discord.__version__}")
        logging.info(f"Invite link: {StrFmt.Cyan}https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=294678424784&scope=bot{StrFmt.Reset}")

while True:
    try:
        with open("config.json") as config_file:
            data = json.load(config_file)
    except FileNotFoundError:
        with open("config.json", "w") as config_file:
            config_file.write(json.dumps( 
                { 
                    "token": "bot_token_here"
                }, indent=4 ))

        logging.error(f"Please fill out config.json file with your bot token!")
        exit()

    token = data["token"]
    config_file.close() # Close handle now, it's not needed anymore

    r = requests.get("https://discord.com/api/v10/users/@me", headers={
        "Authorization": f"Bot {token}"
    })

    data = r.json()
    if data.get("id", None):
        break

    logging.error(f"Invalid token: {data.get('message', 'Unknown error')}")

bot = GatoBot()
bot.run(token, log_handler=None)