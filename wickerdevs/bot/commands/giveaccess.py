from wickerdevs.bot.commands import *

@send_typing_action
def accept_bot_request(update:Update, context:CallbackContext):
    if not check_auth(update, context, admins=True, send=False):
        return

    data = update.callback_query.data
    data = data.split(':')
    # 'ACCEPT:{name}:{user}:{bot_id}': 'Accept'
    user_id = int(data[1])
    user_name = data[2]
    bot_id = int(data[3])
    bot_username = data[4]

    # Give Access
    bot = sheet.get_bot(bot_id)
    if not bot:
        send_message(update, context, error_processing_request_text, message_id=update.callback_query.inline_message_id, parse_mode=ParseMode.HTML)
        return 
    bot.add_user(int(user_id))

    # Notify Developer
    send_message(update, context, access_given_text.format(user_name, user_id, bot_username, bot_id), message_id=update.callback_query.inline_message_id)
    botlogger.debug(f'Notified Developer {update.effective_chat.id}')

    # Notify User
    message_id = sheet.get_message(user_id)
    if message_id:
        try: 
            botlogger.debug(f'Deleted Message for user {user_id}')
            context.bot.delete_message(chat_id=user_id, message_id=message_id)
        except: pass
    message = context.bot.send_message(chat_id=user_id, text=info_access_given_text.format(bot_username), parse_mode=ParseMode.HTML)
    botlogger.debug(f'Sent Message to user {user_id}')
    sheet.set_message(user_id, message.message_id)
    return


@send_typing_action
def decline_bot_request(update:Update, context:CallbackContext):
    if not check_auth(update, context, admins=True, send=False):
        return

    data = update.callback_query.data
    data = data.split(':')
    user_id = int(data[1])
    user_name = data[2]
    bot_id = int(data[3])
    bot_username = data[4]

    # Notify Developer
    send_message(update, context, access_declined_text.format(user_name, user_id, bot_username, bot_id), message_id=update.callback_query.inline_message_id)

    # Notify User
    message_id = sheet.get_message(user_id)
    if message_id:
        try: 
            context.bot.delete_message(chat_id=user_id, message_id=message_id, parse_mode=ParseMode.HTML)
        except: pass
    message = context.bot.send_message(chat_id=user_id, text=info_access_declined_text.format(bot_username), parse_mode=ParseMode.HTML)
    sheet.set_message(user_id, message.message_id)
    return