import time

COOL_DOWN = 15 # in minutes

class AmongUsQueue:
    def __init__(self):
        self.user_time_dict = dict()

    async def add(self, member):
        self.user_time_dict[member] = time.time()
    
    async def remove(self, member):
        self.user_time_dict.pop(member)

    async def update(self):
        for user, u_time in self.user_time_dict.items():
            if time.time() > u_time + (60*COOL_DOWN):
                self.user_time_dict.pop(user)

    async def get_dict(self):
        return self.user_time_dict()

