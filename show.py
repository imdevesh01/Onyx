import os
import discord
import random
import wikipedia
import asyncio
from discord.ext import commands
import os
from googleapiclient.discovery import build
from datetime import time
from discord.ext import commands
import discord, os, asyncio
from datetime import datetime
import youtube_dl

intents = discord.Intents.all()
intents.message_content = True

api_key = "AIzaSyArh3queQVogR1n2BXA-NRsT2RQ0S5MAxg"
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)
queuelist = []
filestodelete = []


#Ping Command
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")


@client.command()
async def greet(ctx):
    await ctx.send("Hey Buddy! How u doin'")


#Coinflip Command
@client.command()
async def coinflip(ctx, call):
    num = random.randint(1, 2)
    res = ''
    call = call.lower()
    if (num == 1):
        res = 'Heads'
    else:
        res = 'Tails'
    if res.lower() == call:
        await ctx.send("It was " + res + "! You WON")
    else:
        await ctx.send("It was " + res + "! Opponent WON")


#Rock Paper Scissors Command
@client.command()
async def rps(ctx, hand):
    hands = ["✌️", "✋", "👊"]
    bothand = random.choice(hands)
    await ctx.send(bothand)
    if hand == bothand:
        await ctx.send("Its a Draw!")
    elif hand == "✌️":
        if bothand == "👊":
            await ctx.send("I won!")
        if bothand == "✋":
            await ctx.send("You won!")
    elif hand == "✋":
        if bothand == "👊":
            await ctx.send("You won!")
        if bothand == "✌️":
            await ctx.send("I won!")
    elif hand == "👊":
        if bothand == "✋":
            await ctx.send("I won!")
        if bothand == "✌️":
            await ctx.send("You won!")


#help Command
@client.command(aliases=["about"])
async def help(ctx):
    MyEmbed = discord.Embed(
        title="Commands",
        description="These are the Commands that you can use for this bot",
        color=discord.Colour.dark_purple())
    MyEmbed.set_thumbnail(
        url=
        "https://is2-ssl.mzstatic.com/image/thumb/Purple125/v4/eb/78/a7/eb78a7b4-0eda-bbf6-0145-1ecee81e9946/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/1200x630wa.png"
    )
    MyEmbed.add_field(
        name="!ping",
        value="This Command replies back with Pong whenever you write !ping.",
        inline=False)
    MyEmbed.add_field(name="!coinflip",
                      value="This Command lets you flip a coin.",
                      inline=False)
    MyEmbed.add_field(
        name="!rps",
        value=
        "This Command allows you to play a game of rock paper scissors with the bot.",
        inline=False)
    
    MyEmbed.add_field(
        name="!show/!pic name",
        value=
        "This Command shows the image of the given name.",
        inline=False)
    
    MyEmbed.add_field(
        name="!wiki name",
        value=
        "This Command provide you the Wikipedia of the given name.",
        inline=False)
    
    MyEmbed.add_field(
        name="!greet",
        value=
        "This Command greets the user.",
        inline=False)
    
    MyEmbed.add_field(
        name="!edit servername name",
        value=
        "This Command changes the name of server to the given name.",
        inline=False)
    
    MyEmbed.add_field(
        name="!edit createvoicechannel name",
        value=
        "This Command creates a voice channel of the given name.",
        inline=False)
    
    MyEmbed.add_field(
        name="!edit createtextechannel name",
        value=
        "This Command creates a text channel of the given name.",
        inline=False)
    
    await ctx.send(embed=MyEmbed)
    
    

#Moderation Bot
@client.group()
async def edit(ctx):
    pass


@edit.command()
async def servername(ctx, *, input):
    await ctx.guild.edit(name=input)


@edit.command()
async def createtextchannel(ctx, *, input):
    await ctx.guild.create_text_channel(name=input)


@edit.command()
async def createvoicechannel(ctx, *, input):
    await ctx.guild.create_voice_channel(name=input)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.kick(member, reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.guild.ban(member, reason=reason)


@client.command()
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(bannedmember.user)


@client.command()
async def purge(ctx,
                amount,
                day: int = None,
                month: int = None,
                year: int = datetime.now().year):
    if amount == "/":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after=datetime(year, month, day))
            print(datetime(year, month, day))
    else:
        await ctx.channel.purge(limit=int(amount) + 1)


@client.command()
async def mute(ctx, user: discord.Member):
    await user.edit(mute=True)


@client.command()
async def unmute(ctx, user: discord.Member):
    await user.edit(mute=False)


@client.command()
async def deafen(ctx, user: discord.Member):
    await user.edit(deafen=True)


@client.command()
async def undeafen(ctx, user: discord.Member):
    await user.edit(deafen=False)


@client.command()
async def voicekick(ctx, user: discord.Member):
    await user.edit(voice_channel=None)


@client.command()
async def wiki(ctx, *, input):
    results = wikipedia.summary(f'of {input}', sentences=4)
    await ctx.send(results)


@client.command(aliases=["show", "pic"])
async def img(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(q=f"{search}",
                           cx="472ea9b78fbdf4759",
                           searchType="image").execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Here Your Image (for {search}) ")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


@client.command(case_insensitive=True,
                aliases=["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files=True, embed_links=True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7)
    seconds = 0
    if reminder is None:
        embed.add_field(
            name='Warning',
            value='Please specify what do you want me to remind you about.'
        )  # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(
            name='Warning',
            value=
            'Please specify a proper duration, send `reminder_help` for more information.'
        )
    elif seconds < 300:
        embed.add_field(
            name='Warning',
            value=
            'You have specified a too short duration!\nMinimum duration is 5 minutes.'
        )
    elif seconds > 7776000:
        embed.add_field(
            name='Warning',
            value=
            'You have specified a too long duration!\nMaximum duration is 90 days.'
        )
    else:
        await ctx.send(
            f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(
            f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)


# Music Bot Code


@client.command()
@commands.has_role("DJ")
async def join(ctx):
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()


@client.command()
@commands.has_role("DJ")
async def leave(ctx, help="leaves the Voice Channel"):
    await ctx.voice_client.disconnect()


@client.command()
@commands.has_role("DJ")
async def play(ctx, *, searchword):
    ydl_opts = {}
    voice = ctx.voice_client

    #Get the Title
    if searchword[0:4] == "http" or searchword[0:3] == "www":
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(searchword, download=False)
            title = info["title"]
            url = searchword

    if searchword[0:4] != "http" and searchword[0:3] != "www":
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{searchword}",
                                    download=False)["entries"][0]
            title = info["title"]
            url = info["webpage_url"]

    ydl_opts = {
        'format':
        'bestaudio/best',
        "outtmpl":
        f"{title}.mp3",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
    }

    #Downloads the Audio File with the Title, it is run in a different thread so that the bot can communicate to the discord server while downloading
    def download(url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, download, url)

    #Playing and Queueing Audio
    if voice.is_playing():
        queuelist.append(title)
        await ctx.send(f"Added to Queue: ** {title} **")
    else:
        voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"),
                   after=lambda e: check_queue())
        await ctx.send(f"Playing ** {title} ** :musical_note:")
        filestodelete.append(title)
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening, name=title))

    #the after function that gets called after the first song ends, then it checks whether a song is in the queuelist
    #if there is a song in the queuelist, it plays that song
    #if there is no song in the queuelist, it deletes all the files in filestodelete
    def check_queue():
        try:
            if queuelist[0] != None:
                voice.play(discord.FFmpegPCMAudio(f"{queuelist[0]}.mp3"),
                           after=lambda e: check_queue())
                coro = client.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.listening, name=queuelist[0]))
                fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
                fut.result()
                filestodelete.append(queuelist[0])
                queuelist.pop(0)
        except IndexError:
            for file in filestodelete:
                os.remove(f"{file}.mp3")
            filestodelete.clear()


#Stop, Resume and Pause
@client.command()
@commands.has_role("DJ")
async def pause(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.pause()
    else:
        await ctx.send("Bot is not playing Audio!")


@client.command(aliases=["skip"])
@commands.has_role("DJ")
async def stop(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        voice.stop()
    else:
        await ctx.send("Bot is not playing Audio!")


@client.command()
@commands.has_role("DJ")
async def resume(ctx):
    voice = ctx.voice_client
    if voice.is_playing() == True:
        await ctx.send("Bot is playing Audio!")
    else:
        voice.resume()


#function that displays the current queue
@client.command()
async def viewqueue(ctx):
    await ctx.send(f"Queue:  ** {str(queuelist)} ** ")


#Error Handlers
@join.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send(
            "You have to be connected to a Voice Channel to use this command.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@leave.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@play.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@stop.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@resume.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@pause.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("Bot is not connected to a Voice Channel.")
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send("You have to have the DJ Role to use this bot.")


@client.command()
async def gif(ctx):
    await ctx.send("Hey!")
async def show_daily_msg():
    now = datetime.now()
    # then = now+datetime.timedelta(days=1)
    # then.replace(hour=7,minute=30)
    then = now.replace(hour = 22, minute=34) # for testing
    wait_time = (then-now).total_seconds()
    await asyncio.sleep(wait_time)
    
    channel1 = client.get_channel(1038495345992274100)
    await channel1.send("Good Morning 🥱")
    
@client.event
async def on_ready():
    await show_daily_msg()

# my_secret = os.environ['TOKEN']
client.run('Token No.')
