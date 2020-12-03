from logging import Filter
from telegram.ext import filters
from telegram.ext.updater import Updater
from wickerdevs.bot.commands.start import * 
from wickerdevs.bot.commands.addbot import *
from wickerdevs.bot.commands.giveaccess import *
from wickerdevs.bot.commands.help import *
from wickerdevs.bot.commands.incorrect import *
from wickerdevs.classes.callbacks import *
from wickerdevs.bot import *
import re


def setup(updater:Updater):
    dp:Dispatcher = updater.dispatcher

    # TODO implement missing methods here
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_def), CommandHandler('requestaccess', start_def), CallbackQueryHandler(start_def, pattern=Callbacks.START)],
        states={
            StartStates.SELECT: [CallbackQueryHandler(select_bot)]
        },
        fallbacks=[CallbackQueryHandler(cancel_start, pattern=Callbacks.CANCEL), MessageHandler(Filters.text, incorrect_command)]
    )


    addbot_handler = ConversationHandler(
        entry_points=[CommandHandler('addbot', addbot_def)],
        states={
            AddBotStates.ID: [MessageHandler(Filters.text, input_addbot_id)],
            AddBotStates.USERNAME: [MessageHandler(Filters.text, input_addbot_username)],
            AddBotStates.DESCRIPTION: [MessageHandler(Filters.text, input_addbot_description)]
        }, 
        fallbacks=[CallbackQueryHandler(cancel_addbot, pattern=Callbacks.CANCEL)]
    )


    # Commands
    dp.add_handler(CommandHandler("help", help_def))
    dp.add_handler(CallbackQueryHandler(accept_bot_request, pattern='ACCEPT'))
    dp.add_handler(CallbackQueryHandler(decline_bot_request, pattern='DECLINE'))
    dp.add_handler(start_handler)
    dp.add_handler(addbot_handler)
    dp.add_handler(MessageHandler(Filters.text, incorrect_command))
    dp.add_handler(MessageHandler(Filters.command, incorrect_command))

    dp.add_error_handler(error)
