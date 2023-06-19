
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db, bot

from webdriver.scheduler import scheduler, scheduler_dashboard

from translate import _



async def add_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        data['days'] = []
        data['time'] = {}
    day_of_week_keyboard = InlineKeyboardMarkup(row_width=3)
    day_of_week=['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    for day in day_of_week:
        day_of_week_keyboard.insert(InlineKeyboardButton(_(User.get_current().id)(day), callback_data=f'day_of_week:{day}'))
    day_of_week_keyboard.row(InlineKeyboardButton(_(User.get_current().id)('continue'), callback_data=f'get_hour'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('set_day_of_week'), reply_markup=day_of_week_keyboard)


#Сохранение дня
async def set_scheduler_day(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        day = call.data.split(':')[1]
        if day not in data['days']:
            data['days'].append(day)
        
        await call.message.edit_text(f"{_(User.get_current().id)('set_day_of_week')}\n{_(User.get_current().id)('сhosen')} {', '.join(list(map(_(User.get_current().id), data['days'])))}",
                                        reply_markup=call.message.reply_markup)
        
#запрос часов
async def get_scheduler_hour(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    hour_keyboard = InlineKeyboardMarkup(row_width=6)
    hour_keyboard.row(InlineKeyboardButton(_(User.get_current().id)('AM'), callback_data=f'AM_PM_switch:'))
    hour_keyboard.row()
    for hour in range (1,13):
        hour_keyboard.insert(InlineKeyboardButton(hour, callback_data=f'hour:{hour}'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('set_hour'), reply_markup=hour_keyboard)
    

# Переключение до/после полудня
async def set_scheduler_AM_PM(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    AM_PM = call.message.reply_markup.inline_keyboard[0][0].text
    if AM_PM == _(User.get_current().id)('AM'):
        AM_PM = _(User.get_current().id)('PM')
    else:
        AM_PM = _(User.get_current().id)('AM')
    call.message.reply_markup.inline_keyboard[0][0].text = AM_PM
    await call.message.edit_reply_markup(call.message.reply_markup)


#Сохранение часов, запрос минут
async def set_scheduler_hour(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        AM_PM = call.message.reply_markup.inline_keyboard[0][0].text
        hour = int(call.data.split(':')[1])
        if AM_PM == _(User.get_current().id)('PM'): 
            hour += 12
        data['time']['hour'] = hour
    minute_keyboard = InlineKeyboardMarkup(row_width=6)
    for minute in range (0,60,5):
        minute_keyboard.insert(InlineKeyboardButton(minute, callback_data=f'minute:{minute}'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('set_minute'), reply_markup=minute_keyboard)



#Сохранение минут, Вопрос о правильности даты
async def set_scheduler_minute(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    time=''
    days=''

    async with state.proxy() as data:
        if not data['days']:
            data['days'] = ['mon', 'tue', 'wed', 'thu', 'fri']
        data['time']['minute'] = int(call.data.split(':')[1])
        days = ', '.join(list(map(_(User.get_current().id), data['days'])))
        minute = data['time']['minute']
        minute = minute if minute > 9 else '0' + str(minute)
        hour = data['time']['hour']
        hour = hour if hour > 9 else '0' + str(hour)
        time = f"{hour}:{minute}"

    yes_no_keyboard = InlineKeyboardMarkup(row_width=2)
    yes_no_keyboard.insert(InlineKeyboardButton( _(User.get_current().id)('yes'), callback_data=f'create_time_sch'))
    yes_no_keyboard.insert(InlineKeyboardButton( _(User.get_current().id)('no'), callback_data=f'add_scheduler'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('confirmation_of_scheduler').format(days, time), reply_markup=yes_no_keyboard)


#создание подписки
async def create_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    file_id = ''
    filters = {}
    async with state.proxy() as data:
        file_id = data['file_id']
        if data.get('filters', None):
            #json_string = {file_id: {}}
            for selector in data['filters']:
                val_list = []
                for val in data['filters'][selector]:
                    val_list.append(list(val.values())[0])
                filters = {**filters, **{selector.split(';')[1]: val_list}}
        scheduler.add_job(scheduler_dashboard, "cron", day_of_week=(','.join(data['days'])), hour=data['time']['hour'], minute=data['time']['minute'], misfire_grace_time = None, replace_existing=True, args=[User.get_current().id, {'docID': file_id, 'path_screenshot':f'{User.get_current().id}_{file_id}.png','filters': filters}],id=f'{User.get_current().id}_{file_id}', name=f'{file_id}')
        await bot.send_message(User.get_current().id, _(User.get_current().id)('scheduler_created'))
        

async def info_about_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    id = call.data.split(':')[1]
    job = scheduler.get_job(id)
    job_keyboard = InlineKeyboardMarkup()
    job_keyboard.add(InlineKeyboardButton( _(User.get_current().id)('info_scheduler'), callback_data=f'info_time_sch:{id}'))
    job_keyboard.add(InlineKeyboardButton( _(User.get_current().id)('delete_scheduler'), callback_data=f'delete_time_sch:{id}'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('info_about_scheduler'), reply_markup=job_keyboard)


async def delete_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    id = call.data.split(':')[1]
    if scheduler.get_job(id):
        scheduler.remove_job(id)
    await bot.send_message(User.get_current().id, _(User.get_current().id)('successfully_deleted'))
    


async def info_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    id = call.data.split(':')[1]
    job = scheduler.get_job(id)
    await bot.send_message(User.get_current().id, str(job))
        

def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_time_scheduler, Text(equals='add_time_sch'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_scheduler_day, Text(startswith='day_of_week:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(get_scheduler_hour, Text(startswith='get_hour'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_scheduler_hour, Text(startswith='hour:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_scheduler_AM_PM, Text(startswith='AM_PM_switch:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_scheduler_minute, Text(startswith='minute:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(create_time_scheduler, Text(equals='create_time_sch'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(info_about_time_scheduler, Text(startswith='info_about_time_sch:'), state='*')
    dp.register_callback_query_handler(info_time_scheduler, Text(startswith='info_time_sch:'), state='*')
    dp.register_callback_query_handler(delete_time_scheduler, Text(startswith='delete_time_sch:'), state='*')