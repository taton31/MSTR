
import sys
sys.path.insert(1, 'C:\\Users\\user\\Desktop\\mstr_bot\\git\\mstr-chat-bot')
import datetime

from database.user_database import *

a = DB('database/bot_database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

# a.insert_date_trigger(4, None)


TRIGGER = 'trigger_2'
q = a.get_all_triggers()
for i in q:

    if i['date_last_update'] and i['trigger_name'] == TRIGGER:
        a.insert_date_trigger(i['ID'], datetime.datetime.now())

