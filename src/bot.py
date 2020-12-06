import discord
from discord import Game
from discord.ext.commands import Bot
import os


BOT_PREFIX = "!"
BOT_TOKEN = os.environ.get('AMONG_US_Q_BOT_TOKEN')

client = Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
client.remove_command('help')

@client.event
async def on_ready():
    """This function runs when the bot is started
    """
    game = discord.Game(name = 'as crewmate')
    await client.change_presence(activity=game)
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



async def on_message(message):
    author = message.author

client.run(BOT_TOKEN)