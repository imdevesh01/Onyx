import discord
import random
import wikipedia
import asyncio
from discord.ext import commands
import os
from googleapiclient.discovery import build
from datetime import time

intents = discord.Intents.all()
intents.message_content = True

api_key = "AIzaSyArh3queQVogR1n2BXA-NRsT2RQ0S5MAxg"
client = commands.Bot(command_prefix="!", help_command=None, intents=intents)
from datetime import datetime


#Ping Command
@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def greet(ctx):
    await ctx.send("Hey Buddy! How u doin'")

#Coinflip Command
@client.command()
async def coinflip(ctx,call):
    num = random.randint(1, 2)
    res=''
    call = call.lower()
    if (num==1):
        res = 'Heads'
    else:
        res = 'Tails'
    if res.lower() == call:
        await ctx.send("It was "+res+"! You WON")
    else:
        await ctx.send("It was "+res+"! Opponent WON")


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


@client.command(aliases=["show","pic"])
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

@client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time,*, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7)
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
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
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)

client.run(
    "MTAxNDg3NzU1MjU1ODQ4OTczMQ.GbwkV6.ks9lmaKt7F_nDu7WI08gVODtwtpmbC66Vp-Rj0")