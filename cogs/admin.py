import discord
from discord import app_commands
from discord.ext import commands

from strformat import StrFmt

import logging

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="annoy",
        description="Nefarious activities"
    )
    @app_commands.default_permissions() # By default this decorator will set permissions to Administrator only
    async def annoy(self, interaction: discord.Interaction, user: discord.User, amount: int = 5):
        # The mention spam can take too long so we'll have the response up here
        # .defer() + .followup.send() can also work but this reply doesn't matter it's only to appease the Discord API
        await interaction.response.send_message("Waking them up...", ephemeral=True, delete_after=5)
        for _ in range(min(amount, 10)):
            await self.bot.get_channel(interaction.channel_id).send(user.mention, delete_after=0.0005)

    @app_commands.command(
        name="shutdown",
        description="Shuts down the bot"
    )
    @app_commands.default_permissions()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("https://tenor.com/view/cat-sleep-good-night-goobnite-gif-21803805", ephemeral=True)
        await self.bot.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        logging.info(f"Message by {message.author} in {message.guild.name} deleted: {StrFmt.Red}{message.content}{StrFmt.Reset}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))