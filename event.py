from email import message
from multiprocessing.connection import Client
import random
import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.message_content = True

bot = discord.Client(intents=intents)
@bot.event
async def on_ready():
    print("Hey! I'm ready to go")
    
@bot.event
async def on_message(msg):
    username = msg.author.display_name
    if(msg.author==bot.user):
        return
    else:
        if(msg.content.lower()=='hello'):
            await msg.channel.send(f'Hi {username}! Nice to meet you.....')

@bot.event
async def on_member_join(member):
    clan = member.guild
    clanname = clan.name
    
    dmchannel = await member.create_dm()
    await dmchannel.send(f'Hey {member.name}! Welcome to {clanname}, We hope you would enjoy your time here :)')
    print(f'{member.name} has joined the server')
    
@bot.event
async def on_raw_reaction_add(payload):
    member = payload.member
    emoji = payload.emoji.name
    message_id=payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    
    if(emoji == "😂" and message_id == 1014897466883178628):
        role = discord.utils.get(guild.roles,name="Happy")
        await member.add_roles(role)
        
    if(emoji == "😔" and message_id == 1014897497572917289):
        role = discord.utils.get(guild.roles,name="Sad")
        await member.add_roles(role)

 
@bot.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id=payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    user = guild.get_member(user_id)
    
    if(emoji == "😂" and message_id == 1014897466883178628):
        role = discord.utils.get(guild.roles,name="Happy")
        await user.remove_roles(role)
        
    if(emoji == "😔" and message_id == 1014897497572917289):
        role = discord.utils.get(guild.roles,name="Sad")
        await user.remove_roles(role)

bot.run('MTAxNDg3NzU1MjU1ODQ4OTczMQ.GbwkV6.ks9lmaKt7F_nDu7WI08gVODtwtpmbC66Vp-Rj0')

