# Import Discord Package
import asyncio
import os
import json
from unicodedata import name
import discord
from discord.ext import commands
# bot
with open("config.json",'r') as config:
    data = json.load(config)
    token = data["TOKEN"]
    emoji = data["emoji"]
    prefix = data["prefix"]
    color = data["color"]
    intents = discord.Intents.default()
    intents.value = data["intents"]

bot = commands.Bot(command_prefix = prefix,intents = intents)

with open("help.json",'r') as f:
    helpData = json.load(f)

# wczytywanie
if os.path.isfile("dane.json"):
    with open("dane.json", "r") as dane:
        bot.dict = json.load(dane) 
else:
    bot.dict = {}

async def savetofile():
    while(True):
        await bot.wait_until_ready()
        with open("dane.json","w") as dane:
            json.dump(bot.dict,dane,indent=3)  
        await asyncio.sleep(600)

def sortdict(dict):
    sortdict = {}
    i = 0
    for student in sorted(dict.items(), key = lambda k_v: k_v[1]["score"],reverse= True):
        pomdict = {}
        pomdict["name"] = student[1]["name"]
        pomdict["score"] = student[1]["score"]
        pomdict["pozycja"] = i
        sortdict[student[0]] = pomdict
        i += 1
    return sortdict
# Start
@bot.event
async def on_ready():
    general_channel = bot.get_channel(969559198063005738)
    await general_channel.send("hello world!")
    bot.dict = sortdict(bot.dict)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=prefix+"helpMe"))
    bot.loop.create_task(savetofile())

#commands
@bot.command(name= 'helpMe')
async def helpFunction(context):
    help_embed = discord.Embed.from_dict(helpData)
    await context.channel.send(embed=help_embed)

@bot.command(name= 'score')
async def score(context):
    dict = bot.dict
    myEmbed = discord.Embed(title = "Score", color = color)
    for student in dict:
        myEmbed.add_field(name = str(dict[student]["pozycja"])+ ": " + dict[student]["name"],value = dict[student]["score"])
    await context.message.channel.send(embed=myEmbed)



@bot.command(name = "myScore")
async def myScore(context):
    dict = bot.dict

    author = context.message.author
    
    try:
        myEmbed = discord.Embed(title = "Score",description = dict[str(author.id)]["score"], color = color)
        myEmbed.add_field(name = "pozycja", value = dict[str(author.id)]["pozycja"])
        myEmbed.set_author(name = author.name)
    except:
        student = {}
        student["name"] = author.name
        student["score"] = 0
        dict[str(author.id)] = student
        myEmbed = discord.Embed(title = "Score",description = dict[str(author.id)]["score"], color = color)
        myEmbed.set_author(name = author.name)
    bot.dict = dict
    await context.message.channel.send(embed=myEmbed)

@bot.command(name = 'save')
async def save(context):
    with open("dane.json","w") as dane:
        json.dump(bot.dict,dane,indent=3)
# events

@bot.event
async def on_reaction_remove(reaction, user):
    dict = bot.dict
    if str(reaction.emoji) == emoji:
        author = reaction.message.author
        aid = author.id
        try:
            dict[str(aid)]["score"] -= 1
            if dict[str(aid)]["name"] != author.name:
                dict[str(aid)]["name"] = author.name
        except:
            student = {}
            student["name"] = author.name
            student["score"] = 0
            dict[str(aid)] = student
    bot.dict = dict
    bot.dict = sortdict(bot.dict)

@bot.event
async def on_reaction_add(reaction, user):
    dict = bot.dict

    if str(reaction.emoji) == emoji:
        author = reaction.message.author
        aid = author.id
        try:
            dict[str(aid)]["score"] += 1
            if dict[str(aid)]["name"] != author.name:
                dict[str(aid)]["name"] = author.name
        except:
            student = {}
            student["name"] = author.name
            student["score"] = 1
            dict[str(aid)] = student
    bot.dict = dict
    bot.dict = sortdict(bot.dict)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# Run the client
bot.run(token)
