# bot.py
import discord
import random
import json
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv("TOKEN")
pairs = {}
dictionaries = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def list_people(message):
    people = message.channel.members
    member_list = []
    for member in people:
        if not member.bot:
            member_list.append(member.name)
    return member_list

async def direct_message(person, match, message):
    member = discord.utils.get(message.guild.members, name=person)
    channel = await member.create_dm()
    #embed=discord.Embed(title="test", description='{}, test'.format(user.mention) , color=0xecce8b)
    #embed.set_image(url=(pfp))
    await channel.send("your secret santa recipient is: " + match)
    #await client.send_message(message.channel, embed=embed)

async def save_names(message, pairs):
    dictionaries[message.guild.name] = pairs
    json_object = json.dumps(dictionaries, indent = 4) 
    with open("dictionaries.json", "w") as outfile: 
        outfile.write(json_object)
    outfile.close()

async def read_json(message):
    try:
        with open("dictionaries.json", "r") as openfile:  
            json_object = json.load(openfile)
        dictionaries = json_object
        pairs = json_object[message.guild.name]
    except:
        return

def shuffle(x):
    copy = x.copy()
    if len(x) == 1:
        raise Exception
    random.shuffle(x)
    for i in range(len(x)):
        if x[i] == copy[i]:
            print(i)
            r = list(range(0,i)) + list(range(i+1, len(x)))
            print(r)
            index = r[random.randint(0, len(r)-1)]
            print(index)
            x[index], x[i] = x[i], x[index]

@client.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.bot:
        return

    elif message.content == '!uses':
        await message.channel.send("usages: !umu, !people, !me, !roll")

    elif message.content == '!juju':
        await message.channel.send("fuck you juju")

    elif message.content == '!umu':
        await message.channel.send('https://www.youtube.com/watch?v=dQ_d_VKrFgM')

    elif message.content == "!people":
        people = message.channel.members
        for member in people:
            if not member.bot:
                await message.channel.send(member.name + " " + member.discriminator)
        await message.channel.send("done")

    elif message.content == "!me":
        if message.author.name in pairs:
            await direct_message(message.author.name, pairs[message.author.name], message)
        else:
            await message.channel.send("Either you are not participating or names have not been rolled.") 

    elif message.content == "!roll":
        await read_json(message)
        if bool(pairs):
            await message.channel.send("Already distributed names.")
            return
        member_list = await list_people(message)
        recipient_list = member_list.copy()
        shuffle(recipient_list)
        for i in range(len(recipient_list)):
            try:
                await direct_message(member_list[i], recipient_list[i], message)
            except:
                await message.channel.send(f"{member_list[i]} cannot receieve a message")
            pairs[member_list[i]] = recipient_list[i]
        await message.channel.send("finished distributing names")
        await save_names(message, pairs)

client.run(TOKEN)
