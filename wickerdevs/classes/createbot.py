from wickerdevs.classes.bot import Bot
from wickerdevs.classes.persistence import Persistence, persistence_decorator


class CreateBot(Persistence):
    def __init__(self, user_id) -> None:
        super().__init__(Persistence.BOT, user_id)
        self.bot = None
        self.id = None
        self.username = None
        self.description = None
        self.users = [user_id]

    @persistence_decorator
    def set_id(self, id):
        self.id = id

    @persistence_decorator
    def set_username(self, username):
        self.username = username

    @persistence_decorator
    def set_users(self, users):
        self.users = users

    @persistence_decorator
    def set_description(self, description):
        self.description = description

    @persistence_decorator
    def set_bot(self):
        self.bot = Bot(self.id, self.username, self.description)
        for user in self.users:
            self.bot.add_user(user)

    