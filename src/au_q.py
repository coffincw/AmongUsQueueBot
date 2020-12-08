import time
import discord


class AmongUsQueue:
    def __init__(self, cooldown):
        '''
        user_time_dict = {
            server_id1: {
                "vc_id": "",
                "cooldown": float # in minutes
                "users": {
                    user1object: [timeadded, context],
                    user2object: [timeadded, context],
                    ...
                }
            }                    
        }
        '''
        self.user_time_dict = dict()

    async def add_server(self, server_id):
        self.user_time_dict[server_id] = dict()
        self.user_time_dict[server_id]["users"] = dict()
        self.user_time_dict[server_id]["vc_id"] = ""
        self.user_time_dict[server_id]["cooldown"] = 15.0

    async def add_player(self, ctx, server_id, player):
        self.user_time_dict[server_id]["users"][ctx.author] = [time.time(), ctx]
    
    async def remove(self, server_id, player):
        self.user_time_dict[server_id]["users"].pop(player)

    async def update_user_time(self, server_id, player):
        ctx = self.user_time_dict[server_id]["users"][player][1]
        self.user_time_dict[server_id]["users"][player] = [time.time(), ctx]

    async def update(self, server_id):
        users_to_remove = set()
        for user, arr in self.user_time_dict[server_id]["users"].items():
            if time.time() > arr[0] + (60*self.user_time_dict[server_id]["cooldown"]):
                users_to_remove.add((user, arr[1]))
        for pair in users_to_remove:
            self.user_time_dict[server_id]["users"].pop(pair[0])
            await pair[1].send(pair[0].mention + ' has been removed from the queue due to inactivity, type !c to re-add')

    async def contains(self, player, server_id):
        has_server = await self.has_server(server_id)
        return has_server and player in self.user_time_dict[server_id]["users"]

    async def has_server(self, server_id):
        return server_id in self.user_time_dict

    async def get_player_dict(self, server_id):
        return self.user_time_dict[server_id]["users"]
    
    async def get_server_ids(self):
        return self.user_time_dict.keys()
    
    async def get_cooldown(self, server_id):
        return self.user_time_dict[server_id]["cooldown"]

    async def set_cooldown(self, server_id, cooldown):
        self.user_time_dict[server_id]["cooldown"] = cooldown
        return cooldown

    async def queue_size(self, server_id):
        has_server = self.has_server(server_id)
        if not has_server:
            return 0
        return len(self.user_time_dict[server_id]["users"])

