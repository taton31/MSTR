import logging


# задаем единый формат сообщениям
formatter = logging.Formatter('\n\n%(asctime)s\tfile name:%(filename)s\tfunction name:%(funcName)s  %(levelname)s: %(message)s')

#создаем логгеры под 4 блока, в кавычках название логгера, которое будет отражаться в лог-файле
webdriver_logger = logging.getLogger('webdriver')
database_logger = logging.getLogger('database')
connection_logger = logging.getLogger('connection')
bot_logger = logging.getLogger('bot')
gmail_logger = logging.getLogger('gmail')

#сюда можно впихнуть общие настройки, пока уровень логирования и формат сообщений
def log_settings(logger, handler):
    logger.setLevel(logging.INFO)
    handler.setFormatter(formatter)

webdriver_handler = logging.FileHandler('log\\webdriver.log') #создаем лог-файл
webdriver_logger.addHandler(webdriver_handler) #соотносим лог-файл с логгером
log_settings(webdriver_logger, webdriver_handler) #задаем настройки
webdriver_logger.setLevel(logging.INFO)

database_handler = logging.FileHandler('log\\database.log')
database_logger.addHandler(database_handler)
log_settings(database_logger, database_handler) 

connection_handler = logging.FileHandler('log\\connection.log')
connection_logger.addHandler(connection_handler)
log_settings(connection_logger, connection_handler) 

bot_handler = logging.FileHandler('log\\bot.log')
bot_logger.addHandler(bot_handler)
log_settings(bot_logger, bot_handler) 

gmail_handler = logging.FileHandler('log\\gmail.log')
gmail_logger.addHandler(gmail_handler)
log_settings(gmail_logger, gmail_handler) 


#тут маленький пример, как можно вынести текст ошибки
if __name__ == '__main__':

    #раскидала сообщения по разным логгерам для примера
    webdriver_logger.debug('debug message')
    database_logger.info('info message')
    connection_logger.warning('warn message')
    bot_logger.error('error message')


    vals = [1, 2]
    try:
        print(vals[4])
    except Exception:
        database_logger.error('error message', exc_info=True)
