from wickerdevs.classes.bot import Bot
from gspread.client import Client
from gspread.models import Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os, re, json, jsonpickle 
from datetime import date, datetime
from wickerdevs import applogger
from wickerdevs.config import secrets



def auth():
    creds_string = secrets.get_var('GSPREAD_CREDS')
    if creds_string == None:
        # use creds to create a client to interact with the Google Drive API
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive']
        # CREDENTIALS HAVE NOT BEEN INITIALIZED BEFORE
        client_secret = os.environ.get('GCLIENT_SECRET')
        if os.environ.get('PORT') in (None, ""):
            # CODE RUNNING LOCALLY
            applogger.debug('DATABASE: Resorted to local JSON file')
            with open('wickerdevs/config/client_secret.json') as json_file:
                client_secret_dict = json.load(json_file)
        else:
            # CODE RUNNING ON SERVER
            client_secret_dict = json.loads(client_secret)

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            client_secret_dict, scope)
        creds_string = jsonpickle.encode(creds)
        secrets.set_var('GSPREAD_CREDS', creds_string)
    creds = jsonpickle.decode(creds_string)
    client = gspread.authorize(creds)

    # IF NO SPREADSHEET ENV VARIABLE HAS BEEN SET, SET UP NEW SPREADSHEET
    if secrets.get_var('SPREADSHEET') == None:
        spreadsheet = set_sheet(client)
        return spreadsheet
    else:
        SPREADSHEET = secrets.get_var('SPREADSHEET')
        spreadsheet = client.open_by_key(SPREADSHEET)
        return spreadsheet


def log(timestamp:datetime, user_id:int or str, action:str):
    spreadsheet = auth()
    logs = spreadsheet.get_worksheet(2)                     
    logs.append_row([str(timestamp), user_id, action])


############################### MESSAGE #################################
def set_message(user_id, message_id):
    spreadsheet = auth()
    sheet:Worksheet = spreadsheet.get_worksheet(1)
    row = find_by_username(user_id, sheet)
    if row:
        sheet.delete_row(row)
    sheet.append_row([user_id, message_id])


def get_message(user_id):
    spreadsheet = auth()
    sheet:Worksheet = spreadsheet.get_worksheet(1)
    row_id = find_by_username(str(user_id), sheet)
    if not row_id:
        return None
    row = get_rows(sheet)[row_id-1]
    message = int(row[1])
    return message


############################### BOTS ###################################
def set_bot(bot:Bot, sheet=None):
    if not sheet:
        spreadsheet = auth()
        sheet:Worksheet = spreadsheet.get_worksheet(0)
    row = find_by_username(bot.bot_id, sheet)
    if row:
        sheet.delete_row(row)
    sheet.append_row([bot.bot_id, bot.serialized()])
    return True


def get_all_bots() -> list:
    spreadsheet = auth()
    sheet:Worksheet = spreadsheet.get_worksheet(0)
    rows = get_rows(sheet)
    bots_data = rows[1:]
    bots = list()
    for data in bots_data:
        bots.append(Bot.from_data(data))
    return bots


def get_bot(bot_id, sheet:Worksheet=None) -> Bot:
    if not sheet:
        spreadsheet = auth()
        sheet:Worksheet = spreadsheet.get_worksheet(0)
    row = find_by_username(bot_id, sheet)
    if not row:
        return None

    rows = get_rows(sheet)
    data = rows[row-1]
    bot:Bot = Bot.from_data(data)
    return bot


############################### GENERAL ################################
def find_by_username(user_id:int, sheet:Worksheet, col:int=1) -> None or int:
    """
    Finds the Row Index within the GSheet Database, matching the ``user_id`` argument.
    Returns None if no record is found.

    Args:
        user_id (int): Telegram ID of the user.
        sheet (Worksheet): Worksheet to check.
        col (int, optional): Column to check. Defaults to 1.

    Returns:
        None or list: None if no record is found, int if the record is found.
    """
    column = sheet.col_values(col)
    rows = list()
    for num, cell in enumerate(column):
        if str(cell) == str(user_id):
            rows.append(num + 1)
    if rows == []:
        return None
    return rows[0]


def get_rows(sheet:Worksheet):
    """
    Get a list of the rows' content from the Google Sheets database.

    :param sheet: GSheets worksheet to get data from
    :type sheet: Worksheet

    :return: List of lists, where each sub-list contains a row's contents.
    :rtype: list
    """
    rows:list = sheet.get_all_values()
    return rows


def get_sheet_url(index:int=0):
    """
    Returns the link of a worksheet

    Args:
        index (int, optional): Index of the sheet to get. Can be either 0, 1 or 2. Defaults to 0.

    Returns:
        str: Url of the selected worksheet
    """
    spreadsheet = auth()
    sheet:Worksheet = spreadsheet.get_worksheet(index)
    url = 'https://docs.google.com/spreadsheets/d/{}/edit#gid={}'.format(spreadsheet.id, sheet.id)
    return url


def set_sheet(client:Client):
    """
    Setup spreadsheet database if none exists yet.
    Will save the spreadsheet ID to Heroku Env Variables or to secrets.json file
    The service email you created throught the Google API will create the new spreadsheet and share it with the email you indicated in the GDRIVE_EMAIL enviroment variable. You will find the spreadsheet database in your google drive shared folder.
    Don't change the order of the worksheets or it will break the code.

    :param client: GSpread client to utilize
    :type client: Client
    :return: The newly created spreadsheet
    :rtype: Spreadsheet
    """
    # CREATE SPREADSHEET
    spreadsheet:Spreadsheet = client.create('FFInstaBot')
    secrets.set_var('SPREADSHEET', spreadsheet.id)

    bots = spreadsheet.add_worksheet(title='Bots', rows=5, cols=2)
    bots.append_row(['BOT ID', 'BOT'])

    messages = spreadsheet.add_worksheet(title='Messages', rows=10, cols=2)
    messages.append_row(['USER ID', 'MESSAGE ID'])

    # CREATE LOGS SHEET
    logs = spreadsheet.add_worksheet(title="Logs", rows=500, cols=3)
    logs.append_row(["TIMESTAMP", "USER ID", "ACTION"])

    # DELETE PRE-EXISTING SHEET
    sheet = spreadsheet.get_worksheet(0)
    spreadsheet.del_worksheet(sheet)

    # SHARE SPREADSHEET
    spreadsheet.share(value=secrets.get_var('GDRIVE_EMAIL'),
                      perm_type="user", role="owner")
    return spreadsheet