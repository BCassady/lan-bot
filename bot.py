# bot.py
import os
from pydoc import describe

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta

import discord 

import random

import pickle

import glob

def save(to_save):
    pickle.dump( to_save, open( "save.p", "wb" ) )

def load():
    return pickle.load( open( "save.p", "rb" ) )

lan = None

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

description = "An amazing bot for tracking LAN"

bot = commands.Bot(command_prefix='!', description=description, help_command=help_command)

# Change only the no_category default string


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='setlan', help='Sets a next LAN time (month, day, year)')
async def set_lan(ctx, month, day, year):

    global lan
    lan = datetime(int(year), int(month), int(day), 20, 0, 0)
    response = "Lan set to " + lan.strftime("%m/%d/%Y") 
    save(lan)
    await ctx.send(response)

@bot.command(name='whenlan', help='Responds with LAN time')
async def when_lan(ctx):

    global lan 
    lan = load()

    if lan == None:
        response = "No LAN :sob:"
    else:
        response = "LAN IS ON " + lan.strftime("%m/%d/%y")
    
    
    await ctx.send(response)

@bot.command(name='cancellan', help='Cancels LAN')
async def cancel_lan(ctx):

    global lan
    lan = None

    response = "LAN Cancelled :sob:"

    save(lan)
    
    await ctx.send(response)

@bot.command(name='timeuntillan', help='Displays the time until LAN')
async def time_until_lan(ctx):

    global lan
    lan = load()

    td = lan - datetime.now()

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    response = "LAN IS IN " + str(days) + " DAYS " + str(hours) + " HOURS " + str(minutes) + " MINUTES " + str(seconds) + " SECONDS" 

    await ctx.send(response)

@bot.command(name='rot', help='Displays random rot wiki link')
async def time_until_lan(ctx):
    choices = pickle.load( open( "realmeye.p", "rb" ) )
    chosen = random.choice(choices)

    await ctx.send("https://www.realmeye.com" + chosen)

@bot.command(name='lan', help='Missing lan right now? Get a random lan image')
async def lan(ctx):
    file_path_type = ["./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.jpeg", "./imgs/*.mov"]
    images = glob.glob(random.choice(file_path_type))

    random_image = random.choice(images)

    with open(random_image, 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

@bot.command(name='8ball', help='Answers any question you have')
async def lan(ctx, question):

    answers = ["Oh yes brudda", "If you go to LAN, yes", "Without a doubt", "Yes", "I would bet my life on it",
    "As likely as the toilet is to be filled at LAN", "As far as I can tell, yes", "No", "Nope", "No shot", "No way brudda",
    "Idk about that one", "This question is too hard for me :sob:", "I cannot decide", "Hell no", "That question is messed up wtf",
    "Oh lawd yes"]

    response = "> " + question + "\n"
    
    response += random.choice(answers)

    await ctx.send(response)
bot.run(TOKEN)
