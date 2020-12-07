import time


class AmongUsQueue:
    def __init__(self, cooldown):
        '''
        user_time_dict = {
                            user1object: [timeadded, context],
                            user2object: [timeadded, context],
                            ...
                         }
        '''
        self.user_time_dict = dict()
        self.cooldown = cooldown # in minutes

    async def add(self, ctx):
        self.user_time_dict[ctx.author] = [time.time(), ctx]
    
    async def remove(self, member):
        self.user_time_dict.pop(member)

    async def update(self):
        users_to_remove = set()
        for user, arr in self.user_time_dict.items():
            if time.time() > arr[0] + (60*self.cooldown):
                users_to_remove.add(user)
        for user in users_to_remove:
            self.user_time_dict.pop(user)
            await arr[1].send(user.mention + ' has been removed from the queue due to inactivity, type !c to re-add')

    async def get_dict(self):
        return self.user_time_dict
    
    async def get_cooldown(self):
        return self.cooldown

    async def set_cooldown(self, cooldown):
        self.cooldown = cooldown

    async def size(self):
        return len(self.user_time_dict)

