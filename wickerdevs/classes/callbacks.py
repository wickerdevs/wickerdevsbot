class Callbacks:
    """Object to store PTB conversations Callbacks"""
    CANCEL = 'CANCEL'
    NONE = 'NONE'
    DONE= 'DONE'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    CONFIRM = 'CONFIRM'
    # COMMANDS
    START = 'START'


class StartStates:
    """Object to store PTB Start Conversation Handler states indicators"""
    SELECT = 1


class Objects:
    PERSISTENCE = 1
    BOT = 2


class AddBotStates:
    ID = 1
    USERNAME = 2
    DESCRIPTION = 3