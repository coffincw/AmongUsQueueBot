import discord
import au_q
import asyncio
import time

'''
{user1, user2}
'''
COOLDOWN = 15.0 #minutes
user_queue = au_q.AmongUsQueue(COOLDOWN)

async def update_set(client):
    while True:
        ids = await user_queue.get_server_ids()
        for server_id in ids:
            vc_id = await user_queue.get_voice_channel_id(server_id)
            if vc_id != -1:
                guild = client.get_guild(server_id)
                connected_players = discord.utils.get(guild.channels, id=vc_id, type=discord.ChannelType.voice).members
                print(connected_players)
                for player in connected_players:
                    has_player = await user_queue.contains(player, server_id)
                    if has_player:
                        await user_queue.update_user_time(server_id, player)
                    else:
                        await user_queue.add_player(None, server_id, player)
            size = await user_queue.queue_size(server_id)
            prev_size = await user_queue.get_prev_size(server_id)
            await user_queue.set_prev_size(server_id, size)
            if size != 0 and size != prev_size:
                await user_queue.update(server_id)
                if size == 5:
                    await ping_users(server_id, 5)
                if size == 8:
                    await ping_users(server_id, 8)
                if size == 9:
                    await ping_users(server_id, 9)
                if size == 10:
                    await ping_users(server_id, 10)
        await asyncio.sleep(10)

async def list_queue(ctx):
    server_id = ctx.message.guild.id
    user_dict = await user_queue.get_player_dict(server_id)
    cooldown = await user_queue.get_cooldown(server_id)
    description = "!c to add yourself, !d to leave\n\n"
    # Players who don\'t send a message in the server\nfor " + \
    #              (str(int(cooldown)) if cooldown.is_integer() else str(cooldown)) + " minutes will be dropped"
    
    if len(user_dict) == 0:
        description += "**No players in the queue**"
        # embed.add_field(
        #     name="No players in the queue", 
        #     value="-----")
    else:
        spot = 1
        for user, arr in user_dict.items():
            description += "**" + str(spot) + ". " + user.display_name + "**\n"
            spot += 1
            #num_min = (time.time() - arr[0]) / 60
            #num_seconds = (time.time()-arr[0]) % 60
            # embed.add_field(
            #     name=user.display_name, 
            #     value="Added " + str(int(num_min)) + "m " + str(int(num_seconds)) + "s ago",
            #     inline=False)
    embed = discord.Embed(
        title="Among Us Queue [" + str(len(user_dict)) + "/10]", 
        description=description, 
        color=discord.Color.blurple())

    embed.set_footer(
        text="Updated " + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime()) + " UTC")

    await ctx.send(embed=embed)


async def add_to_queue(ctx):
    player = ctx.author # get the author of the command
    server_id = ctx.message.guild.id
    await user_queue.add_player(server_id, player)
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

async def set_waiting_room(ctx, arg):
    server_id = ctx.message.guild.id
    voice_channel = discord.utils.get(ctx.message.guild.channels, name=arg, type=discord.ChannelType.voice)
    if voice_channel is None:
        await ctx.send(embed=discord.Embed(
            description="Can't find voice channel with the name " + arg,
            color=discord.Color.red()))
        return
    channel_id = voice_channel.id
    await user_queue.set_voice_channel_id(server_id, channel_id)
    description = "Waiting room channel set to: " + voice_channel.name
    await ctx.send(embed=discord.Embed(
        description=description, 
        color=discord.Color.green()))

async def set_text_channel(ctx, arg):
    server_id = ctx.message.guild.id
    text_channel = discord.utils.get(ctx.message.guild.channels, name=arg, type=discord.ChannelType.text)
    if text_channel is None:
        await ctx.send(embed=discord.Embed(
            description="Can't find text channel with the name " + arg,
            color=discord.Color.red()))
        return
    await user_queue.set_text_channel(server_id, text_channel)
    description = "Queue text channel set to: " + text_channel.name
    await ctx.send(embed=discord.Embed(
        description=description, 
        color=discord.Color.green()))

async def ping_users(server_id, size):
    tc = await user_queue.get_text_channel(server_id)
    await tc.send(str(tc.guild.default_role) + " " + str(10-size) + " more available spots")

async def ping_queue_players(ctx):
    server_id = ctx.message.guild.id
    player_dict = await user_queue.get_player_dict(server_id)
    if len(player_dict) == 0:
        await ctx.send(embed=discord.Embed(
            description="No users in the queue",
            color=discord.Color.red()))
        return
    mention_message = ""
    for players in player_dict.keys():
        mention_message += players.mention + " "
    await ctx.send(mention_message)