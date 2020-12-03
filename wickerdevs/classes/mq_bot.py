from wickerdevs.config import secrets
from wickerdevs.texts import *
from wickerdevs.modules import sheet
import telegram.bot, logging
from telegram.ext import messagequeue as mq 
from telegram import ParseMode

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MQBot(telegram.bot.Bot):
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()
        logger.debug(f'BOT ID: {super(MQBot, self).id}')
    
    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_queued_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)

    def request_access(self, user, name, bot_id):
        users_str = secrets.get_var('DEVS')
        if isinstance(users_str, str):
            users_str.replace('[', '')
            users_str.replace(']', '')
            users_str.replace(' ', '')
            users = users_str.split(',')
            for index, user in enumerate(users):
                users[index] = int(user)
        else:
            users = users_str
        
        name.replace(' ', '\\n')
        bot = sheet.get_bot(bot_id)
        if bot:
            from wickerdevs.classes.forwarder_markup import CreateMarkup
            text = request_access_text.format(user, name, bot.username)
            success = False
            for dev in users:
                markup = CreateMarkup({
                    f'ACCEPT:{user}:{name}:{bot_id}:{bot.username}': 'Accept',
                    f'DECLINE:{user}:{name}:{bot_id}:{bot.username}': 'Decline'
                }).create_markup()
                try:
                    self.send_queued_message(chat_id=dev, text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
                    success = True
                except: pass
            return success
        else:
            return False

    def report_error(self, error=None, send_screenshot=False, screenshot_name=''):
        string = str(secrets.get_var('DEVS')).replace('[', '')
        string = string.replace(']', '')
        string = string.replace(' ', '')
        devs = list(string.split(','))
        for dev in devs:
            if send_screenshot:
                self.send_photo(chat_id=int(dev), photo=open('{}.png'.format(screenshot_name), 'rb'), caption='There was an error with the wickerdevs: \n{}'.format(error))
            else:
                self.send_message(chat_id=int(dev), text='There was an error with the wickerdevs: \n{}'.format(error), parse_mode=ParseMode.HTML)