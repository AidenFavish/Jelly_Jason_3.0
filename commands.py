import json
import discord
import datetime
import asyncio


async def custom_commands(message, client):
    msg = message.content.lower()
    with open("storage.json", "r") as j:
        data = json.load(j)

    if "-add " in msg:
        command = msg[len("-add "):]

        # Separates the trigger word from the response phrase
        trigger = ""
        response = ""
        for i in range(0, len(command)):
            if command[i:i + 1] == " ":
                response = command[i + 1:]
                break
            else:
                trigger += command[i:i + 1]

        # Adds the command to the dictionary
        with open("storage.json", "r") as j:
            data = json.load(j)

        data["Commands"][trigger] = response

        with open("storage.json", "w") as j:
            json.dump(data, j)

        await message.delete()
    elif "-delete " in msg:
        trigger = msg[len("-delete "):]

        with open("storage.json", "r") as j:
            data = json.load(j)

        data["Commands"].pop(trigger)

        with open("storage.json", "w") as j:
            json.dump(data, j)

        await message.delete()
    elif msg == "-help" or msg == "-commands" or msg == "-info":
        display1 = "```fix\nCOMPLEX COMMANDS:\n-add *trigger_word* *response_phrase* -> adds a command with a trigger word of at least 3 words" \
            "\n-delete *trigger_word* -> deletes the command associated with the trigger word" \
            "\n-watching *rest of status* -> changes my status to watching *rest of status*```"

        await message.channel.send(display1)
        master = "ALL SIMPLE COMMANDS:"
        with open("storage.json", "r") as j:
            data = json.load(j)
        for i in data["Commands"]:
            if len(master + "\n" + i + " -> " + data["Commands"][i]) <= 1900:
                master = master + "\n" + i + " -> " + data["Commands"][i]
            else:
                await message.channel.send(master)
                master = i + " -> " + data["Commands"][i]
        await message.channel.send(master)
        await message.channel.send("These are just the public commands, there are more hidden commands")
    elif "-watching " in msg:
        status = msg[len("-watching "):]

        with open("storage.json", "r") as j:
            data = json.load(j)

        data["Status"] = status

        with open("storage.json", "w") as j:
            json.dump(data, j)

        activity = discord.Activity(type=discord.ActivityType.watching, name=" " + data["Status"])
        await client.change_presence(status=discord.Status.online, activity=activity)
    elif msg in data["Commands"]:
        await message.channel.send(data["Commands"][msg])


async def statistics(client):
    counterC = client.get_channel(958155533955780659)
    with open("storage.json", "r") as j:
        data = json.load(j)
    messageBoard = counterC.get_partial_message("1051588395165548544")
    display = ""

    block1 = "```yaml\n" + str(data["MainCounter"]) + " total server messages (Not including bots)```"
    block2 = "```fix"
    block4 = "```ini\n[ Last updated: " + str(datetime.datetime.now()) + " ]```"

    memoryDict = {}
    while data["MsgCounter"]:
        holder = [0, 0]
        for i in data["MsgCounter"]:
            if data["MsgCounter"][i] >= holder[1]:
                holder = [i, data["MsgCounter"][i]]
        memoryDict[holder[0]] = holder[1]
        del data["MsgCounter"][holder[0]]
    data["MsgCounter"] = memoryDict
    counter = 1
    for i in data["MsgCounter"]:
        user = client.get_user(int(i))
        if user == None:
            user = client.user
        block2 += "\n" + str(counter) + ". " + user.name + " -> " + str(data["MsgCounter"][i]) + " messages"
        counter += 1
    block2 += "```"
    display = block1 + block2 + block4
    await messageBoard.edit(content=display)


async def log(message, client):
    gml = client.get_channel(955166586090696734)
    author = str(message.author.id)
    with open("storage.json", "r") as j:
        data = json.load(j)

    embed = discord.Embed(title=message.author.name + "#" + message.author.discriminator, url=message.jump_url,
                          description=message.content, color=message.author.top_role.color)
    await gml.send(embed=embed)
    data["MainCounter"] += 1

    # Updates the counters by author and by server
    if author not in data["MsgCounter"]:
        data["MsgCounter"][author] = 1
    else:
        data["MsgCounter"][author] += 1

    with open("storage.json", "w") as j:
        json.dump(data, j)

    await statistics(client)


async def stalker(client):
    stalkerChannel = client.get_channel(954982395721949184)
    with open("storage.json", "r") as j:
        data = json.load(j)
    for i in stalkerChannel.guild.members:
        if str(i.id) not in data["Stalker"]:
            data["Stalker"][str(i.id)] = str(i.status)
        if data["Stalker"][str(i.id)] != str(i.status):
            data["Stalker"][str(i.id)] = str(i.status)
            await stalkerChannel.send(i.name + " is now " + str(i.status) + " at " + str(datetime.datetime.now()))
    with open("storage.json", "w") as j:
        json.dump(data, j)
    await asyncio.sleep(30)
    asyncio.create_task(stalker(client))
