import os, logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
applogger = logging.getLogger(__name__)
applogger.setLevel(logging.DEBUG)

LOCALHOST = True
if os.environ.get('PORT') not in (None, ""):
    # Code running locally
    LOCALHOST = False

from telegram.ext import Updater, Defaults
from telegram import ParseMode
from telegram.utils.request import Request
from wickerdevs.classes.mq_bot import MQBot
from telegram.ext import messagequeue as mq

# Initialize Bot
from wickerdevs.config import secrets
BOT_TOKEN = secrets.get_var('BOT_TOKEN')
URL = secrets.get_var('SERVER_APP_DOMAIN')
PORT = int(os.environ.get('PORT', 5000))
from wickerdevs.bot import telebot

# set connection pool size for bot 
request = Request(con_pool_size=8)
q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
defaults = Defaults(parse_mode=ParseMode.HTML, run_async=True)
telegram_bot = MQBot(BOT_TOKEN, request=request, mqueue=q, defaults=defaults)
updater = Updater(bot=telegram_bot, use_context=True, defaults=defaults)


# SET UP BOT COMMAND HANDLERS
telebot.setup(updater)
        