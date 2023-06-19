import connect
import telebot

bot = telebot.TeleBot('5098007657:AAEwiPhBn7k-CR8q4FtPSYPJFNwrUEyGDxk');


connection = connect.connect()
#a=connect.search_rep(connection, 'TG')
'''
print(a)
for i in a: 
    print(i.name) 
 '''

report_list={}
report_df={}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Я могу найти отчет, напиши /search")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "!!!")
    elif message.text.lower() == "/search":
        bot.send_message(message.from_user.id, "Введи имя отчета")
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message): #получаем фамилию
    global report_list
    report_list[message.from_user.id]=connect.search_rep(connection, message.text)
    for i in report_list[message.from_user.id]: 
        bot.send_message(message.from_user.id, i.name) 
    bot.send_message(message.from_user.id, 'Нужный отчет?')
    bot.register_next_step_handler(message, IsIt)


def IsIt(message):
    if message.text.lower() == "да":
        bot.send_message(message.from_user.id, "точно?")
        bot.register_next_step_handler(message, get_data)
    elif message.text.lower() == "нет":
        bot.send_message(message.from_user.id, "вводи точнее \nПовтори ввод")
        bot.register_next_step_handler(message, get_name)


def get_data(message):
    global report_df
    report_df[message.from_user.id] = report_list[message.from_user.id][0].to_dataframe()
    bot.send_message(message.from_user.id, 'Какой показатель вывести?')
    bot.send_message(message.from_user.id, *list(report_df[message.from_user.id]))
    bot.register_next_step_handler(message, get_data2)

def get_data2(message):
    global report_df
    bot.send_message(message.from_user.id, 'Получай')
    bot.send_message(message.from_user.id, report_df[message.from_user.id].loc[message.text])
    #bot.register_next_step_handler(message, get_data2)


bot.polling(none_stop=True, interval=0)


