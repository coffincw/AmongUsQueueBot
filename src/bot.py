import discord
from discord import Game
from discord.ext.commands import Bot
import os
import queue_commands as q
import asyncio


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
    client.loop.create_task(q.update_set())


async def on_message(message):
    author = message.author

@client.command(name='c')
async def add_to_queue(ctx):
    await q.add_to_queue(ctx)

@client.command(name='d')
async def remove_from_queue(ctx):
    await q.remove_from_queue(ctx)

@client.command(name='l')
async def list_queue(ctx):
    await q.list_queue(ctx)

@client.command(name='uc')
async def update_cooldown(ctx, arg):
    await q.update_cooldown(ctx, arg)


client.run(BOT_TOKEN)