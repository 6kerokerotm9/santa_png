# bot.py
import discord
import random
import json
import os
from dotenv import load_dotenv


class MyClient(discord.Client):
    pairs = {}
    dictionaries = {}

    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def list_people(self, message):
        people = message.guild.members
        member_list = []
        for member in people:
            if not member.bot:
                member_list.append(member.name)
        return member_list

    async def direct_message(self, person, match, message):
        member = discord.utils.get(message.guild.members, name=person)
        channel = await member.create_dm()
        await channel.send(match)

    async def save_names(self, message, pairs):
        self.dictionaries[message.guild.name] = self.pairs
        json_object = json.dumps(self.dictionaries, indent = 4) 
        with open("dictionaries.json", "w") as outfile: 
            outfile.write(json_object)
        outfile.close()

    async def read_json(self, message):
        try:
            with open("dictionaries.json", "r") as openfile:  
                json_object = json.load(openfile)
            self.dictionaries = json_object
            self.pairs = json_object[message.guild.name]
        except:
            return

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        elif message.content == 'umu':
            await message.channel.send('roma')
        
        elif message.content == '!quit' or message.content == '!stop' or message.content == '!exit':
            print("quitting out")
            await client.logout()

        elif message.content == "!people":
            people = message.guild.members
            for member in people:
                if not member.bot:
                    await message.channel.send(member.name + " " + member.discriminator)

        elif message.content == "!me":
            if message.author.name in self.pairs:
                await self.direct_message(message.author.name, self.pairs[message.author.name], message)
            else:
                await message.channel.send("Either you are not participating or names have not been rolled.") 

        elif message.content == "!roll":
            await self.read_json(message)
            if bool(self.pairs):
                await message.channel.send("Already distributed names.")
                return
            member_list = await self.list_people(message)
            recipient_list = await self.list_people(message)
            for people in member_list:
                match = people
                while(match == people):
                    index = random.randint(0, len(recipient_list)-1)
                    match = recipient_list[index]
                recipient_list.remove(match)
                await self.direct_message(people, match, message)
                self.pairs[people] = match
            await message.channel.send("finished distributing names")
            await self.save_names(message, self.pairs)

client = MyClient()
load_dotenv()
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
