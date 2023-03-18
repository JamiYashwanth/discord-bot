import discord
from scraping import *
from user_model import *
from convert_mongodata_to_excle import  *
import os
from services.future_constest_service import *
from services.user_profile_service import *
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='#', intents=intents)

import time
TOKEN = 'MTA3MjIwMzM4OTEyMDgyMzI5Ng.GBYYob.sK_gCGdfNLv3bYGCVEIUjpjeT00VN4hf3z_a88'

@bot.command(name='hello', aliases=['hi'], description='Says hello to the user.')
async def hello_command(message):
    username = str(message.author).split('#')[0]
    await message.channel.send(f'Hello {username}')

@bot.command(name='rankings',description='rankings of a particular contest')
async def rankings_command(message):
    message=message.message
    user_message = str(message.content)
    await message.channel.send('Generating Excel sheet , Please wait for some time....')
    contest_id = user_message.split(' ')[1].upper()
    if(check_if_contest_exists_in_db(contest_id)):
        convert_to_excel(contest_id)
        channel = bot.get_channel(1081879142636736572)
        await channel.send(file=discord.File(f'ranklist.xlsx'))
    else:
        scrape(contest_id,'A')
        scrape(contest_id,'B')
        scrape(contest_id,'C')
        scrape(contest_id,'D')
        convert_to_excel(contest_id)
        channel = bot.get_channel(1081879142636736572)
        await channel.send(file=discord.File(f'ranklist.xlsx'))

@bot.command(name='myrankings',description='rankings of a particular contest')
async def myrankings(message):
    message=message.message
    user_message = str(message.content)
    platform = user_message.split(' ')[1]
    userName = user_message.split(' ')[2]
    wait_message = await message.channel.send(f'Generating data for your rankings of {platform}')
    embed = discord.Embed(title='Your ranking till now', description=userRankings(platform, userName), color=discord.Color.green())
    await wait_message.delete()
    await message.channel.send(embed=embed)

@bot.command(name='plot')
async def plot(message):
    message=message.message
    user_message = str(message.content)
    userName = user_message.split(' ')[1]
    duration = user_message.split(' ')[2]
    wait_message = await message.channel.send(f'Generating your {duration} graph')
    graphGenerationUser(userName,duration)
    await wait_message.delete()
    await message.channel.send(file=discord.File(f'C:/Users/jamiy/PycharmProjects/pythonProject/bar.png'))

@bot.command(name='compare')
async def compare(message):
    message=message.message
    user_message = str(message.content)
    userName1 = user_message.split(' ')[1]
    userName2 = user_message.split(' ')[2]
    duration = user_message.split(' ')[3]
    graphsGenerationComparision(userName1,userName2,duration)
    await message.channel.send(file = discord.File(f'C:/Users/jamiy/PycharmProjects/pythonProject/bar.png'))

@bot.command(name='contests')
async def contests(message):
    message=message.message
    user_message = str(message.content)
    wait_message = await message.channel.send('Wait a minute ...')
    host = user_message.split(' ')[1]
    contests = contestHost(host)
    embededMessage = discord.Embed(title=f"{host.capitalize()} Contests", description=contests, color=0x00ff00, )
    await wait_message.delete()
    await message.channel.send(embed=embededMessage)

@bot.command(name='user')
async def user(message):
    message=message.message
    user_message = str(message.content)
    wait_message = await message.channel.send('Wait a minute ...')
    host = user_message.split(' ')[1]
    user = user_message.split(' ')[2]
    obj = User(user, host)
    data = obj.get_info()
    embededMessage = discord.Embed(title="Profile", description=data, color=0x00ff00, )
    embededMessage.set_image(url = obj._image)
    await wait_message.delete()
    await message.channel.send(embed=embededMessage)

bot.run(TOKEN)

