import gettext

en = gettext.translation("tg_bot", localedir="locale", languages=['en'])
ru = gettext.translation("tg_bot", localedir="locale", languages=['ru'])


en.install()
ru.install()
en_translate = en.gettext
ru_translate = ru.gettext

def _ (language:str = 'ru'):
    return en_translate if language=='en' else ru_translate if language=='ru' else None

# _(local)('text')
# local ='ru'