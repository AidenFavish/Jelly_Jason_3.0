from time import sleep
import random
import discord
from HiddenData import token
import json
import commands

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
intents.invites = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("I'm in")
    print(client.user)
    with open("storage.json", "r") as j:
        data = json.load(j)
    activity = discord.Activity(type=discord.ActivityType.watching, name=" " + data["Status"])
    await client.change_presence(status=discord.Status.online, activity=activity)
    await commands.stalker(client)


@client.event
async def on_message(message):
    # Makes sure Jason doesn't read his own messages
    if message.author.id != client.user.id:
        await commands.custom_commands(message, client)

        # Blacklists testing channel to prevent diluting of the grand message log
        if message.channel.id != 948350259896143883:
            await commands.log(message, client)


client.run(token)
