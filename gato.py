# GatoBot - couldntbe.me

# Standard imports
import os
import glob
import logging
import json
import requests

# Discord imports
import discord
from discord.ext import commands

# Our imports
from helpers import StrFmt

# Use Discord.py's prewritten logger format
discord.utils.setup_logging()

class GatoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='hey gato, ', # Unused
            intents=discord.Intents.all()
        )

        self.token = ""
        self.path  = os.path.dirname(os.path.realpath(__file__))

        self.loaded_cogs = {}

        logging.info("Loading config...")
        self.load_config()

    async def setup_hook(self):
        logging.info("Loading cogs...")

        cogs = glob.glob((self.path + "/cogs/") + "*.py")
        for i, path in enumerate(cogs):
            cog_name = os.path.basename(path).replace(".py", "")
            ext = "cogs." + cog_name

            try:
                await self.load_extension(ext)
            except discord.DiscordException as error:
                logging.error(f"Failed to load cog \"{ext}\" ({error})")
                self.loaded_cogs[cog_name] = {"ext": ext, "loaded": False}
            else:
                logging.info(f"[{i + 1}/{len(cogs)}] Loaded {ext}")
                self.loaded_cogs[cog_name] = {"ext": ext, "loaded": True}

        if len(self.loaded_cogs) == len(cogs):
            logging.info("All cogs loaded successfully")
        else:
            logging.error(f"Loaded {len(self.loaded_cogs)}/{len(cogs)} cogs - please check console")

        await self.tree.sync()

    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info(f"Discord.py version: {discord.__version__}")
        logging.info(f"Invite link: {StrFmt.Cyan}https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=294678424784&scope=bot{StrFmt.Reset}")

    def load_config(self):
        # Try to load config, if it doesn't exist, create one & retry
        for _ in range(2):
            try:
                with open("config.json", encoding="utf-8") as config_file:
                    data = json.load(config_file)
            except FileNotFoundError:
                logging.error("Config not found, creating one...")
                with open("config.json", "w", encoding="utf-8") as config_file:
                    new_token = input("Please enter your bot token: ")

                    config_file.write(json.dumps(
                        {
                            "token": new_token
                        }, indent=4 ))

                    logging.info("Token saved to config, reloading...")
                    continue
            break

        self.token = data["token"]
        config_file.close() # Close handle now, it's not needed anymore

        response = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bot {self.token}",
        }, timeout=30)

        data = response.json()
        if data.get("id", None):
            logging.info("Config loaded")
            return

        logging.error(f"Invalid token: {data.get('message', 'Unknown error')}")

    def run(self):
        super().run(self.token, log_handler=None)

def main():
    bot = GatoBot()
    bot.run()

if __name__ == "__main__":
    main()
