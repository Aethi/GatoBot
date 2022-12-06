import discord
import requests
from discord import app_commands
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="cat", description="Get a random cat image")
    async def cat(self, interaction: discord.Interaction, tag: str = None) -> None:
        # Grab a random cat via Cat as a service
        url = "https://cataas.com/cat?json=true" if tag is None else f"https://cataas.com/cat/{tag}?json=true"

        response = requests.get(url, headers={"accept": "*/*"}, timeout=10)
        if response.status_code == 404:
            default = requests.get("https://cataas.com/cat?json=true", headers={"accept": "*/*"}, timeout=10)
            img_url = "https://cataas.com" + default.json()["url"]

            return await interaction.response.send_message(f"Tag not found - here's a random cat {img_url}")

        # Sends the link to the image page to the user, Discord will auto-embed this
        img_url = "https://cataas.com" + response.json()["url"]
        await interaction.response.send_message(img_url)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
