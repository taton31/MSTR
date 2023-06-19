import gettext
from create_bot_and_conn import db

en = gettext.translation("tg_botEN", localedir="locale", languages=['en'])
ru = gettext.translation("tg_botRU", localedir="locale", languages=['ru'])

en.install()
ru.install()
en_translate = en.gettext
ru_translate = ru.gettext


def _(user_id: str = 'ru'):
    lan = db.get_language(user_id)
    return en_translate if lan == 'en' else ru_translate if lan == 'ru' else ru_translate 


# _(local)('text')
# local ='ru'
