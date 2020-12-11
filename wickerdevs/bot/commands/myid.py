from wickerdevs.bot.commands import *

def myid_def(update, context):
    send_message(update, context, id_info_text.format(update.effective_user.id))