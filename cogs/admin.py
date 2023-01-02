import logging

import discord
from discord import app_commands
from discord.ext import commands

from modules.helpers import StrFmt as fmt

class Admin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="annoy", description="Nefarious activities")
    @app_commands.default_permissions()  # By default this decorator will set permissions to Administrator only
    async def annoy(self, interaction: discord.Interaction, user: discord.User, amount: int = 5):
        # The mention spam can take too long so we'll have the response up here
        # .defer() + .followup.send() can also work but this reply doesn't matter it's only to appease the Discord API
        await interaction.response.send_message("Waking them up...", ephemeral=True, delete_after=5)
        for _ in range(min(amount, 10)):
            await self.bot.get_channel(interaction.channel_id).send(user.mention, delete_after=0.0005)

    @app_commands.command(name="purge", description="Purge messages from a channel")
    @app_commands.default_permissions()
    async def purge(self, interaction: discord.Interaction, amount: int = 10):
        await interaction.response.send_message(f"Removing {amount} messages...", ephemeral=True, delete_after=8)
        await interaction.channel.purge(limit=min(amount, 100))

    @app_commands.command(name="shutdown", description="Shuts down the bot")
    @app_commands.default_permissions()
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("https://tenor.com/view/cat-sleep-good-night-goobnite-gif-21803805", ephemeral=True)
        await self.bot.close()

    @app_commands.command(name="load", description="Loads a cog")
    @app_commands.default_permissions()
    async def load(self, interaction: discord.Interaction, cog: str) -> None:
        try:
            cog_str = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.load_extension(cog_str)
            self.bot.loaded_cogs[cog]['loaded'] = True
        except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotFound, commands.NoEntryPointError, commands.ExtensionFailed) as error:
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message(f"\\✔️ Loaded ***{cog_str}***", ephemeral=True)

    @app_commands.command(name="reload", description="Reloads a cog")
    @app_commands.default_permissions()
    async def reload(self, interaction: discord.Interaction, cog: str) -> None:
        try:
            # Avoid locking out cog management
            if cog == "admin":
                await interaction.response.send_message("cogs.admin is a required cog", ephemeral=True)
                return

            cog_str = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.reload_extension(cog_str)
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound, commands.NoEntryPointError, commands.ExtensionFailed) as error:
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message(f"\\🔄 Reloaded ***{cog_str}***", ephemeral=True)

    @app_commands.command(name="unload", description="Unloads a cog")
    @app_commands.default_permissions()
    async def unload(self, interaction: discord.Interaction, cog: str) -> None:
        try:
            # Avoid locking out cog management
            if cog == "admin":
                await interaction.response.send_message("cogs.admin is a required cog", ephemeral=True)
                return

            cog_str = f"cogs.{cog}" if not cog.startswith("cogs.") else cog
            await self.bot.unload_extension(cog_str)
            self.bot.loaded_cogs[cog]['loaded'] = False
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound) as error:
            await interaction.response.send_message(f"{error}", ephemeral=True)
        else:
            await interaction.response.send_message(f"\\❌ Unloaded ***{cog_str}***\n", ephemeral=True)

    @app_commands.command(name="cogs", description="Lists all cogs")
    @app_commands.default_permissions()
    async def cogs(self, interaction: discord.Interaction):
        cogs = self.bot.loaded_cogs
        cog_list = ""

        for cog, info in cogs:
            if info['loaded']:
                cog_list += f"\\✔️ {cog.capitalize()}\n"
            else:
                cog_list += f"\\❌ {cog.capitalize()}\n"

        await interaction.response.send_message(cog_list, ephemeral=True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        logging.info(f"Message by {message.author} in {message.guild.name} deleted: {fmt.Red}{message.content}{fmt.Reset}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
