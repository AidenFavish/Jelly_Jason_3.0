from time import sleep
import random
import discord
from HiddenData import token
import json
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)
    with open("storage.json", "r") as j:
        data = json.load(j)
    activity = discord.Activity(type=discord.ActivityType.watching, name=" " + data["Status"])
    await client.change_presence(status=discord.Status.online, activity=activity)