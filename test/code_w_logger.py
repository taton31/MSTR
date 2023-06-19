"""import logging

# задаем единый формат сообщениям
formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')

#создаем логгеры под 4 блока, в кавычках название логгера, которое будет отражаться в лог-файле
scr_logger = logging.getLogger('screenshots')
base_logger = logging.getLogger('database')
connect_logger = logging.getLogger('mstr_connect')
tg_logger = logging.getLogger('tg bot')

#сюда можно впихнуть общие настройки, пока уровень логирования и формат сообщений
def log_settings(logger, handler):
    logger.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

scr_handler = logging.FileHandler('screenshots.log') #создаем лог-файл
scr_logger.addHandler(scr_handler) #соотносим лог-файл с логгером
log_settings(scr_logger, scr_handler) #задаем настройки

base_handler = logging.FileHandler('database.log')
base_logger.addHandler(base_handler)
log_settings(base_logger, base_handler) #задаем настройки

base_logger.error('%s\t\t\terror occured with connection to base ', "44", exc_info=True)
oshibka(user)"""