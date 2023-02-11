import discord
from scraping import *
from user_model import *
import os
from services.future_constest_service import *
from services.user_profile_service import * 

import time
TOKEN = 'MTA3MjIwMzM4OTEyMDgyMzI5Ng.GBYYob.sK_gCGdfNLv3bYGCVEIUjpjeT00VN4hf3z_a88'
#
client = discord.Client(intents=discord.Intents.default())
#
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    if user_message == 'Hi':
        await message.channel.send(f'Hello {username}')
        return
    if user_message.startswith('rankings'):
        await message.channel.send('Generating Excel sheet , Please wait for some time....')
        contest_id = user_message.split(' ')[1].upper()
        path = f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_id}_rankings.xlsx'
        isExisting = os.path.exists(path)
        if(isExisting):
            await message.channel.send(file=discord.File(f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_id}_rankings.xlsx'))
            return
        else:
            scrape(contest_id,'A')
            scrape(contest_id,'B')
            scrape(contest_id,'C')
            scrape(contest_id,'D')
            await message.channel.send(file=discord.File(f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_id}_rankings.xlsx'))
        return
    if user_message.startswith('myRankings') :
        platform = user_message.split(' ')[1]
        userName = user_message.split(' ')[2]
        await message.channel.send(f'Generating data for your rankings of {platform}')
        await message.channel.send(userRankings(platform, userName))
        return
    if user_message.startswith('contests'): 
        await message.channel.send('Wait a minute ...') 
        host = user_message.split(' ')[1] 
        contests = contestHost(host)
        embededMessage = discord.Embed(title=f"{host.capitalize()} Contests", description=contests, color=0x00ff00, )
        await message.channel.send(embed=embededMessage)
        return
    if user_message.startswith('user'): 
        await message.channel.send('Wait a minute ...') 
        host = user_message.split(' ')[1] 
        user = user_message.split(' ')[2]
        obj = User(user, host) 
        data = obj.get_info()
        embededMessage = discord.Embed(title="Profile", description=data, color=0x00ff00, )
        embededMessage.set_image(url = obj._image)
        await message.channel.send(embed=embededMessage)
        return

client.run(TOKEN)
