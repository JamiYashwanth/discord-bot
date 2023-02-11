import discord
from scraping import *
from user_model import *
import os
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


client.run(TOKEN)
