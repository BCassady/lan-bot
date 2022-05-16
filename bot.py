# bot.py
import os
from pydoc import describe

from discord.ext import commands
from dotenv import load_dotenv
from datetime import date, datetime
from datetime import timedelta

from pytz import timezone

import asyncio

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
async def lan(ctx, *, question):

    answers = ["Oh yes brudda", "If you go to LAN, yes", "Without a doubt", "Yes", "I would bet my life on it",
    "As likely as the toilet is to be filled at LAN", "As far as I can tell, yes", "No", "Nope", "No shot", "No way brudda", "Hell no",
    "Oh lawd yes"]

    response = "> " + question + "\n"
    
    response += random.choice(answers)

    await ctx.send(response)

WHEN = datetime.time(15, 0, 0)  # 3:00 PM
channel_id = 715038755211444324 

async def called_once_a_day():  # Fired every day
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_channel(channel_id) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    td = lan - datetime.now()
    days = td.days
    await channel.send("OMG LAN IN " + str(days))

async def background_task():
    now = datetime.now(timezone('US/Central'))
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), datetime.time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

bot.run(TOKEN)
