from wickerdevs.classes.createbot import CreateBot
from wickerdevs.bot.commands import *


@send_typing_action
def addbot_def(update:Update, context):
    if not check_auth(update, context, admins=True):
        return ConversationHandler.END
    
    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
    message = send_message(update, context, input_id_text, markup)
    createbot = CreateBot(update.effective_user.id)
    createbot.set_message(message.message_id)
    return AddBotStates.ID


@send_typing_action
def input_addbot_id(update, context):
    createbot:CreateBot = CreateBot.deserialize(Persistence.BOT, update)
    if not createbot:
        return
    
    data = update.message.text
    createbot.set_id(int(data))

    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
    message = send_message(update, context, input_botusername_text, markup, createbot.get_message_id())
    createbot.set_message(message.message_id)
    return AddBotStates.USERNAME


@send_typing_action
def input_addbot_username(update, context):
    createbot:CreateBot = CreateBot.deserialize(Persistence.BOT, update)
    if not createbot:
        return
    
    createbot.set_username(update.message.text)
    
    # Ask for description
    markup = CreateMarkup({Callbacks.CANCEL: 'Cancel'}).create_markup()
    message = send_message(update, context, input_botdescription_text, markup, createbot.get_message_id())
    createbot.set_message(message.message_id)
    return AddBotStates.DESCRIPTION


@send_typing_action
def input_addbot_description(update, context):
    createbot:CreateBot = CreateBot.deserialize(Persistence.BOT, update)
    if not createbot:
        return
    
    createbot.set_description(update.message.text)
    createbot.set_bot()
    
    # Ask for description
    message = send_message(update, context, bot_saved_text, message_id=createbot.get_message_id())
    createbot.discard()
    return ConversationHandler.END


@send_typing_action
def cancel_addbot(update, context, createbot:CreateBot=None):
    if not createbot:
        createbot:CreateBot = CreateBot.deserialize(Persistence.BOT, update)
        message_id = createbot.get_message_id()
    else:
        message_id = None
    send_message(update, context, cancel_createbot_text, message_id=message_id)

    return ConversationHandler.END
    