import time
import discord


class AmongUsQueue:
    def __init__(self, cooldown):
        '''
        user_time_dict = {
            server_id1: {
                "vc_id": -1,
                "cooldown": float # in minutes
                "tc": None,
                "prev_size": 0
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
        self.user_time_dict[server_id]["vc_id"] = -1
        self.user_time_dict[server_id]["tc"] = None
        self.user_time_dict[server_id]["prev_size"] = 0
        self.user_time_dict[server_id]["cooldown"] = 15.0

    async def add_player(self, server_id, player):
        self.user_time_dict[server_id]["users"][player] = time.time()
    
    async def remove(self, server_id, player):
        self.user_time_dict[server_id]["users"].pop(player)

    async def clear(self, server_id):
        self.user_time_dict[server_id]["users"].clear()

    async def update_user_time(self, server_id, player):
        self.user_time_dict[server_id]["users"][player] = time.time()

    async def update(self, server_id):
        users_to_remove = set()
        print("Current Time: " + str(time.time()))
        for user, u_time in self.user_time_dict[server_id]["users"].items():
            print("Kick " + user.display_name + " out of the queue: " + str(u_time + (60*self.user_time_dict[server_id]["cooldown"])))
            if time.time() > u_time + (60*self.user_time_dict[server_id]["cooldown"]):
                users_to_remove.add(user)
        for user in users_to_remove:
            self.user_time_dict[server_id]["users"].pop(user)
            if self.user_time_dict[server_id]["tc"] is not None:
                await self.user_time_dict[server_id]["tc"].send(user.mention + ' has been removed from the queue due to inactivity, type !c to re-add')

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

    async def set_voice_channel_id(self, server_id, vc_id):
        self.user_time_dict[server_id]["vc_id"] = vc_id
    
    async def get_voice_channel_id(self, server_id):
        return self.user_time_dict[server_id]["vc_id"]

    async def set_text_channel(self, server_id, tc):
        self.user_time_dict[server_id]["tc"] = tc

    async def get_text_channel(self, server_id):
        return self.user_time_dict[server_id]["tc"]

    async def set_prev_size(self, server_id, new_size):
        self.user_time_dict[server_id]["prev_size"] = new_size

    async def get_prev_size(self, server_id):
        return self.user_time_dict[server_id]["prev_size"]

    async def queue_size(self, server_id):
        has_server = self.has_server(server_id)
        if not has_server:
            return 0
        return len(self.user_time_dict[server_id]["users"])

