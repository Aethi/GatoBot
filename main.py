'''
    GatoBot

    Todo:
        - Clean up code by separating into modules/cogs
        - Find some APIs to use for fun commands
        - Add permission bits to config file
'''

import asyncio
import random
import logging
import requests
import json

import discord
from discord import app_commands, Intents, Client, Interaction

class StrFmt:
    Reset       = '\033[0m'
    # Colors
    Cyan        = '\033[96m'
    Purple      = '\033[95m'
    Blue        = '\033[94m'
    Yellow      = '\033[93m'
    Green       = '\033[92m'
    Red         = '\033[91m'
    # Decorators
    Bold        = '\033[1m'
    Underline   = '\033[4m'

#
# Setup
#

async def change_bot_presence():
    await client.wait_until_ready()

    servers  = "server" if len(client.guilds) == 1 else "servers"
    gremlins = "gremlin" if len(client.users) == 1 else "gremlins"

    status = {
        1: {"Activity": discord.ActivityType.watching,  
            "Status": ["cat videos", f"{len(client.users)} {gremlins} in {len(client.guilds)} {servers}", "Jerma compilations", "the demons in my puter"]},

        2: {"Activity": discord.ActivityType.playing,   
            "Status": ["with cats", "Madden NFL 06 on XBOX", "with lasers"]},

        3: {"Activity": discord.ActivityType.listening, 
            "Status": ["the screams of the damned", f"cat activation noise compilation #{random.randint(1, 1000)}"]},
    }

    index    = random.randint( 1, 3 )
    activity = status[index]["Activity"]
    string   = random.choice(status[index]["Status"])

    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(
            type=activity, name=string
        ))
        await asyncio.sleep(60 * 5) # 5 minutes

class Gato(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self) -> None:
        # This is called when the bot boots, to setup the global commands
        await self.tree.sync(guild=None)
        self.loop.create_task(change_bot_presence())

# Variable to store the bot class and interact with it
client = Gato(intents=Intents.all())

# Discord.py library can set up logging for us, so we can just use that
discord.utils.setup_logging()

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

#
# Listeners
#

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user} (ID: {client.user.id})")
    logging.info(f"Discord.py version: {discord.__version__}")
    logging.info(f"Invite link: {StrFmt.Cyan}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=294678424784&scope=bot{StrFmt.Reset}" )

@client.event
async def on_message_delete(message):
    if message.author.bot:
        return

    logging.info(f"Message by {message.author} in {message.guild.name} deleted: {StrFmt.Red}{message.content}{StrFmt.Reset}")

@client.event
async def on_message(message):
    if not message.content or not message.author or message.author.bot:
        return # Don't process garbage

    if "@everyone" in message.content or "@here" in message.content: # .mention_everyone fails on unsuccessful mentions, so we do it manually
        await message.reply("🖕")

    if client.user in message.mentions and not message.mention_everyone:
        if "wyd" in message.content.lower():
            await message.reply("nm u?")
        else:
            await message.reply(random.choice([
                "hiiiiii omggg hii heyy heyihiih iiiihii",
                "https://i.imgur.com/socchQU.mp4",
                "https://tenor.com/view/hello-chat-cat-gif-22139058",
                "https://media.discordapp.net/attachments/1041527309959712830/1041542572537036870/DC5DE324-9FAF-4B54-AD5B-40EEABEFF6A0.gif"
            ]))

    # Stolen from Frost
    if message.content.startswith("^") or message.content.lower() == "this":
        if message.content == "^" or "this" in message.content.lower():
            await message.channel.send(random.choice([ "^", "^ this" ]))

    if message.content.lower() == "f":
        await message.channel.send("F")

    if "thanks for the invite" in message.content.lower():
        await message.channel.send(f"{message.author.mention} shut the fuck up")

#
# Commands
#

@client.tree.command(description="Los gatos 🐱")
async def cat(interaction: Interaction):
    # Grab a random cat via Cat as a service
    r = requests.get("https://cataas.com/cat?json=true", headers={
        "accept": f"*/*"
    })

    # Send the cat back to the user
    await interaction.response.send_message("https://cataas.com" + r.json()["url"]) # TODO: Proper embed for gif support, possibly add args for tags

@client.tree.command(description="Nefarious activity")
@app_commands.default_permissions() # Default to administrator only
async def annoy(interaction: Interaction, user: discord.User, amount: int = 5):
    await interaction.response.send_message("Waking them up...", ephemeral=True, delete_after=3) # Slash commands require a response
    for _i in range(min(amount, 10)):
        await client.get_channel(interaction.channel_id).send(user.mention, delete_after=0.0005)

@client.tree.command(description="Closes connection to discord")
@app_commands.default_permissions()
async def shutdown(interaction: Interaction):
    await interaction.response.send_message("https://tenor.com/view/cat-sleep-good-night-goobnite-gif-21803805")
    await client.close()

@client.tree.command(description="Retrieve information about a user (blank = server)")
async def info(interaction: Interaction, user: discord.Member = None):
    if user == None:
        guild = client.get_guild(interaction.guild_id)
        embed = discord.Embed(title=guild.name, description="Server information", color=0x4169E1)
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Region", value=guild.preferred_locale, inline=True)
        embed.add_field(name="Created at", value=guild.created_at.strftime("%b %d, %Y %I:%M %p"), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Text channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Categories", value=len(guild.categories), inline=True)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)
    else:
        if user.bot:
            return await interaction.response.send_message("🤖", ephemeral=True)

        embed = discord.Embed(title=user.name, description="User information", color=0x4169E1)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Created at", value=user.created_at.strftime("%b %d, %Y %I:%M %p"), inline=True)
        embed.add_field(name="Joined at", value=user.joined_at.strftime("%b %d, %Y %I:%M %p"), inline=True)
        embed.add_field(name="Roles", value=", ".join(filter(lambda x: not "@everyone" in x.lower(), [role.name for role in user.roles])), inline=True)
        embed.add_field(name="Flags", value=", ".join([flag.name for flag in user.public_flags.all()]), inline=True)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

#
# Run the bot
#

client.run(token, log_handler=None)