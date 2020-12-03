from wickerdevs.bot.commands import *


@send_typing_action
def start_def(update:Update, context:CallbackContext):
    if check_auth(update, context, admins=True, send=False):
        update.effective_chat.send_message(text=user_is_admin_no_start_text)
        try: update.message.delete()
        except: pass
        return ConversationHandler.END

    # GET BOTS MARKUP
    bots = sheet.get_all_bots()
    available = list()
    
    markup_dict = {}
    for bot in bots:
        if update.effective_user.id not in bot.users:
            markup_dict[bot.bot_id] = bot.username
            available.append(bot)
        
    if len(available) < 1:
        send_message(update, context, no_bots_available)
        return ConversationHandler.END

    markup_dict[Callbacks.CANCEL] = 'Cancel'
    markup = CreateMarkup(markup_dict).create_markup()
    send_message(update, context, select_bot_text, markup)
    return StartStates.SELECT


@send_typing_action
def select_bot(update:Update, context:CallbackContext):
    data = update.callback_query.data
    if data == Callbacks.CANCEL:
        return cancel_start(update, context)
    else:
        id = data

    bot:Bot = sheet.get_bot(id)
    if not bot:
        markup = CreateMarkup({Callbacks.START: 'Try Again'})
        send_message(update, context, bot_not_available, markup)
        return ConversationHandler.END

    result = context.bot.request_access(update.effective_user.id, update.effective_user.full_name, id)
    if result:
        send_message(update, context, request_sent.format(bot.username))
    else:
        send_message(update, context, request_error_text)
    return ConversationHandler.END


def cancel_start(update, context):
    send_message(update, context, cancelled_start)
    return ConversationHandler.END