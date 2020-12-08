import discord
import au_q
import asyncio
import time

'''
{user1, user2}
'''
COOLDOWN = 15.0 #minutes
user_queue = au_q.AmongUsQueue(COOLDOWN)

async def update_set():
    while True:
        ids = await user_queue.get_server_ids()
        for server_id in ids:
            size = await user_queue.queue_size(server_id)
            if size != 0:
                await user_queue.update(server_id)
        await asyncio.sleep(10)

async def list_queue(ctx):
    server_id = ctx.message.guild.id
    user_dict = await user_queue.get_player_dict(server_id)
    cooldown = await user_queue.get_cooldown(server_id)
    description = "!c to add yourself, !d to leave\nPlayers who don\'t send a message in the server\nfor " + \
                  (str(int(cooldown)) if cooldown.is_integer() else str(cooldown)) + " minutes will be dropped"
    embed = discord.Embed(
        title="Among Us Queue [" + str(len(user_dict)) + "/10]", 
        description=description, 
        color=discord.Color.blurple())
    if len(user_dict) == 0:
        embed.add_field(
            name="No players in the queue", 
            value="-----")
    else:
        for user, arr in user_dict.items():
            num_min = (time.time() - arr[0]) / 60
            num_seconds = (time.time()-arr[0]) % 60
            embed.add_field(
                name=user.display_name, 
                value="Added " + str(int(num_min)) + "m " + str(int(num_seconds)) + "s ago",
                inline=False)

    embed.set_footer(
        text="Updated " + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime()) + " UTC")

    await ctx.send(embed=embed)


async def add_to_queue(ctx):
    player = ctx.author # get the author of the command
    server_id = ctx.message.guild.id
    has_id = await user_queue.has_server(server_id)
    if not has_id:
        await user_queue.add_server(server_id)
    await user_queue.add_player(ctx, server_id, player)
    await list_queue(ctx)

async def remove_from_queue(ctx):
    player = ctx.author # get the author of the command
    server_id = ctx.message.guild.id
    has_player = await user_queue.contains(player, server_id)
    if not has_player:
        await ctx.send(embed=discord.Embed(
            description="Player isn't currently in the queue.",
            color=discord.Color.red()))
    else:
        await user_queue.remove(server_id, player)
    await list_queue(ctx)

async def update_cooldown(ctx, cooldown):
    server_id = ctx.message.guild.id
    if not cooldown.isnumeric():
        await ctx.send(embed=discord.Embed(
            description="Please enter a number, example: !uc 15",
            color=discord.Color.red()))
        return
    prev_cooldown = await user_queue.get_cooldown(server_id)
    new_cooldown = await user_queue.set_cooldown(server_id, float(cooldown))
    description = "Cooldown changed from " + (str(int(prev_cooldown)) if prev_cooldown.is_integer() else str(prev_cooldown)) + \
                  " minutes to " + (str(int(new_cooldown)) if new_cooldown.is_integer() else str(new_cooldown)) + " minutes."
    await ctx.send(embed=discord.Embed(
        description=description, 
        color=discord.Color.green()))