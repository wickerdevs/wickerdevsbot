from wickerdevs.bot.commands import *

@send_typing_action
def help_def(update, context):
    send_message(update, context, help_text)