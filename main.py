import discord
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
    if user_message == 'ranking':
        await message.channel.send('Will be soon...')
        return

client.run(TOKEN)
