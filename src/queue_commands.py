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
        size = await user_queue.size()
        if size != 0:
            await user_queue.update()
        await asyncio.sleep(10)

async def list_queue(ctx):
    user_dict = await user_queue.get_dict()
    cooldown = await user_queue.get_cooldown()
    description = "!c to add yourself, !d to leave\nPlayers who don\'t send a message in the server\nfor " + \
                  (str(int(cooldown)) if cooldown.is_integer() else str(cooldown)) + " minutes will be dropped"
    embed = discord.Embed(title="Among Us Queue", description=description, color=discord.Color.teal())
    if len(user_dict) == 0:
        embed.add_field(name="No players in the queue", value="-----")
    else:
        for user, arr in user_dict.items():
            num_min = (time.time() - arr[0]) / 60
            num_seconds = (time.time()-arr[0]) % 60
            embed.add_field(name=user.display_name, value="Added " + str(int(num_min)) + "m " + str(int(num_seconds)) + "s ago")

    embed.set_footer(text="Updated " + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime()) + " UTC")

    await ctx.send(embed=embed)


async def add_to_queue(ctx):
    await user_queue.add(ctx)
    await list_queue(ctx)

async def remove_from_queue(ctx):
    player = ctx.author # get the author of the command
    await user_queue.remove(player)
    await list_queue(ctx)

async def update_cooldown(ctx, cooldown):
    if not cooldown.isnumeric():
        await ctx.send(embed=discord.Embed(description="Please enter a number, example: !uc 15", color=discord.Color.red()))
        return
    await user_queue.set_cooldown(float(cooldown))