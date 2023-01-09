import os
from pytube import YouTube, exceptions

import discord
from discord import app_commands
from discord.ext import commands

class Media(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.tmp_dir = os.path.join(os.getcwd(), "tmp")

    @app_commands.command(name="ytdl", description="Download a YouTube video")
    async def ytdl(self, interaction: discord.Interaction, url: str, audio: bool = False) -> None:
        youtube = YouTube(url)

        await interaction.response.send_message(f"Downloading {youtube.title}...")

        if youtube.age_restricted is True:
            try:
                youtube.bypass_age_gate()
            except exceptions.AgeRestrictedError as error:
                return await self.bot.get_channel(interaction.channel_id).send(f"{error}")

        path = youtube.streams.get_highest_resolution().download(output_path=self.tmp_dir)

        if audio:
            base, _ = os.path.splitext(path)
            new_file = base + '.mp3'
            os.rename(path, new_file)

            path = new_file

        try:
            await self.bot.get_channel(interaction.channel_id).send(f"Downloaded {youtube.title}", file=discord.File(path))
        except discord.errors.HTTPException as error:
            # 413 Payload too large -- 8MB limit for standard users, 50MB for lvl2 boosted server, 100MB for lvl3 boosted server
            if error.code == 40005:
                await self.bot.get_channel(interaction.channel_id).send(f"File too large to send ({(os.path.getsize(path) / 1048576):.3} MB)")

        os.remove(path)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Media(bot))
