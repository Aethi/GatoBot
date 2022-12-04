import discord
from discord import app_commands
from discord.ext import commands

import requests

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="cat",
        description="Get a random cat image"
    )
    async def cat(self, interaction: discord.Interaction):
        # Grab a random cat via Cat as a service
        r = requests.get("https://cataas.com/cat?json=true", headers={
            "accept": f"*/*"
        })

        # Sends the direct link to the image to the user, Discord will auto-embed this
        # TODO: Add a way to grab the direct file url instead of this weird indirect link - this should be faster and support gifs.
        # TODO: Add tags for fun
        await interaction.response.send_message("https://cataas.com" + r.json()["url"])

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))