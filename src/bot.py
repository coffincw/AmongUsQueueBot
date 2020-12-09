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
    client.loop.create_task(q.update_set(client))

@client.event
async def on_message(message):
    author = message.author
    server_id = message.guild.id
    has_server = await q.user_queue.has_server(server_id)
    if not has_server:
        await q.user_queue.add_server(server_id)
    # if the user is in the queue update their time to 
    # indicate they're active
    has_author = await q.user_queue.contains(author, server_id)
    if has_author:
        await q.user_queue.update_user_time(server_id, author)
    await client.process_commands(message)



@client.command(name='h', aliases=['help'])
async def help(ctx):
    '''
    Help command to display all the commands
    '''
    embed = discord.Embed(
        color = discord.Color.orange()
    )
    embed.set_author(name='Help', icon_url='https://cdn.discordapp.com/attachments/552254229419393036/785392866657697812/bot_logo.png')

    COMMANDS = {
        '!c': 'Adds yourself to the queue',
        '!d': 'Removes yourself from the queue',
        '!q': 'Displays the current queue including how long each player has been in the queue',
        '!sc [minutes]': 'Sets the cooldown to remove players from the queue to *minutes*'
    }
    for c, desc in COMMANDS.items():
        embed.add_field(
            name = c,
            value = desc,
            inline = False
        )
    await ctx.send(embed=embed)


@client.command(name='c', aliases=['can'])
async def add_to_queue(ctx):
    '''
    Add the calling user to the player queue
    '''
    await q.add_to_queue(ctx)

@client.command(name='d', aliases=['drop'])
async def remove_from_queue(ctx):
    '''
    Removes the calling user from the player queue
    '''
    await q.remove_from_queue(ctx)

@client.command(name='q', aliases=['queue'])
async def list_queue(ctx):
    '''
    Displays the current queue including how long each player has been in the queue
    '''
    await q.list_queue(ctx)

@client.command(name='sc', aliases=['setcooldown'])
async def update_cooldown(ctx, arg):
    '''
    Sets the cooldown to remove players from the queue to *arg*
    '''
    await q.update_cooldown(ctx, arg)

@client.command(name='swc', aliases=['setwaitchannel', 'setwait'])
async def set_wait_channel(ctx, arg):
    '''
    Sets the waiting room voice channel for resetting connected users cooldown
    '''
    await q.set_waiting_room(ctx, arg)


client.run(BOT_TOKEN)