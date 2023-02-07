import discord
from scraping import *
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
        scrape(contest_id,'A')
        scrape(contest_id,'B')
        scrape(contest_id,'C')
        scrape(contest_id,'D')
        await message.channel.send(file=discord.File(f'{contest_id}_rankings.xlsx'))
        return

client.run(TOKEN)
