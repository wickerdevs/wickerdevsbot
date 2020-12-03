from datetime import datetime
import jsonpickle
from wickerdevs import applogger
from functools import wraps

class Bot():
    def __init__(self, bot_id:int, username:str, description:str, users:list=[]) -> None:
        self.bot_id = bot_id
        self.username = username
        self.description = description
        self.users = users

    @staticmethod
    def from_data(data:list):
        if isinstance(data, list) and len(data) == 2:
            data = data[1]
        
        try:
            return jsonpickle.decode(data)
        except:
            applogger.warn(f'Failed decoding Bot object from data. DATA: {data}')
            return None

    def serialized(self):
        return jsonpickle.encode(self)

    def __str__(self) -> str:
        return jsonpickle.encode(self)

    def __sheet_persist(func): #TODO might return error if self not in arguments
        @wraps(func)
        def wrapper(cls, *args, **kwargs):
            result = func(cls, *args, **kwargs)
            from wickerdevs.modules import sheet
            sheet.set_bot(cls)
            try:
                user = args[0]
            except:
                user = kwargs['user']
                
            if func.__name__ == 'add_user':
                string = f'ACCESS GIVEN TO {user}'
            else:
                string = f'ACCESS REVOKED FROM {user}'
            sheet.log(datetime.utcnow(), cls.bot_id, string)
            return result
        return wrapper

    @__sheet_persist
    def add_user(self, user):
        self.users.append(user)
        return True

    @__sheet_persist
    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
            return True
        return False

        

