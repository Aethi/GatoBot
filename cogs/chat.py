import discord
from discord.ext import commands

import random

class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # Don't process garbage
        if not message.content or not message.author or message.author.bot:
            return

        # .mention_everyone fails on unsuccessful mentions, so we do it manually
        if "@everyone" in message.content or "@here" in message.content:
            await message.reply("🖕")

        if self.bot.user in message.mentions and not message.mention_everyone:
            if "wyd" in message.content.lower():
                await message.reply("nm u?")
            else:
                await message.reply(random.choice([
                    "hiiiiii omggg hii heyy heyihiih iiiihii",
                    "https://i.imgur.com/socchQU.mp4",
                    "https://tenor.com/view/hello-chat-cat-gif-22139058",
                    "https://media.discordapp.net/attachments/1041527309959712830/1041542572537036870/DC5DE324-9FAF-4B54-AD5B-40EEABEFF6A0.gif"
                ]))

        # My favorite CBot feature
        # https://github.com/FFrost/CBot/blob/master/cogs/messages.py#L54
        if message.content.startswith("^") or message.content.lower() == "this":
            await message.channel.send(random.choice([ "^", "^ this" ]))

        if message.content.lower() == "f":
            await message.channel.send("F")

        if "thanks for the invite" in message.content.lower():
            await message.channel.send(f"{message.author.mention} shut the fuck up")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Chat(bot))