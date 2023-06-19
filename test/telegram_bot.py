

import random
import asyncio
import time
from webbrowser import BaseBrowser
from pyppeteer import launch
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from mstrio.types import ObjectTypes, ObjectSubTypes
import mstr_connect
import aiogram as aio
from pyppeteer import launch
import screenshot
from screenshot import get_selectors, get_values, on_startup, create_page, get_filter_screen
from aiogram.dispatcher.filters.state import StatesGroup, State

#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'0105984311EA440357CD0080EF354C4B','docType': 'document','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
#asyncio.get_event_loop().run_until_complete(screenshot.screenshot({'headless': True,'docID':'743FFE22314887C8F2407C9B559ECB4C','docType': 'dossier','path': 'https://dashboard-temp.corp.mvideo.ru:443/MicroStrategy/servlet/mstrWeb' ,'Server':'10.191.2.88', 'Project': '%D0%94%D0%B0%D1%88%D0%B1%D0%BE%D1%80%D0%B4%D1%8B%20%D0%BE%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%B0', 'password':'Ceo143566'}))
asyncio.get_event_loop().run_until_complete(on_startup(''))

asyncio.get_event_loop().run_until_complete(create_page(1,{'docID': 'EA706ACB43C4530927380DB3B07E0889'}) )

#asyncio.get_event_loop().run_until_complete(get_filter_screen(1))
asyncio.get_event_loop().run_until_complete(create_page(2,{'docID': '8CD564B54D2ED4AFD358F3853610D647'}) )
asyncio.get_event_loop().run_until_complete(get_filter_screen(2))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(1))
asyncio.get_event_loop().run_until_complete(get_filter_screen(1, {'security': ['ACADEMY DINOSAUR', 'ACE GOLDFINGER'], 'filters': {'IGK719A420311EA16852B700080EF55FCB9':['h1;264614C648E9C743C4283B8137C8D9BA','h10;264614C648E9C743C4283B8137C8D9BA']}}))
#asyncio.get_event_loop().run_until_complete(get_filter_screen(2))


time.sleep(22222)
exit()
token = '5149682661:AAFYq2BpHTSfIYrU2wjKfUT8zn4aDe_1FIU'
bot = aio.Bot(token)
dp = aio.Dispatcher(bot, storage=MemoryStorage())
conn = mstr_connect.get_connection()


class get_info(StatesGroup):
    find_name = State()
    file_data = State()
    final = State()


@dp.message_handler(commands=['start'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введите /search для поиска отчета,\n/help для списка доступных команд')
    #keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Нужная кнопка', callback_data='document_233DB69981444C2B38E266AF39289366'))
    #await bot.send_message(message.from_user.id, 'нажми', reply_markup=keyboard)
    #await get_info.file_data.set()



@dp.message_handler(commands=['search'])
async def start_message(message: aio.types.Message):
    await bot.send_message(message.from_user.id, 'Введи имя отчета:')
    await get_info.find_name.set()


@dp.message_handler(commands=['help'])
async def help_info(message: aio.types.Message):
    await bot.send_message(message.from_user.id, f'Список доступных команд:\n /search - поиск отчета')


@dp.message_handler(state=get_info.find_name)
async def search_report(message: aio.types.Message, state: FSMContext):
    all_reports_keyboard = InlineKeyboardMarkup()
    all_documents_keyboard = InlineKeyboardMarkup()
    all_reports = mstr_connect.search_report(conn, message.text)
    all_documents = mstr_connect.search_document(conn, message.text)

    async with state.proxy() as data:
        data['find_name'] = message.text
    #print(len(all_reports))
    for report in all_reports:
        if report.subtype == 768:
            all_reports_keyboard.add(InlineKeyboardButton(report.name, callback_data=f'report_{report.id}'))
    for document in all_documents:
        all_documents_keyboard.add(InlineKeyboardButton(document.name, callback_data=f'document_{document.id}'))
    if len(all_reports) != 0:
        await bot.send_message(message.from_user.id, 'Список доступных репортов:', reply_markup=all_reports_keyboard)
    if len(all_documents) != 0:
        await bot.send_message(message.from_user.id, 'Список доступных документов:', reply_markup=all_documents_keyboard)
    await get_info.file_data.set()


@dp.callback_query_handler(Text(startswith=['report_', 'document_']), state=get_info.file_data)
async def get_screenshot(call: aio.types.CallbackQuery, state: FSMContext):
    #print(call.data)
    # await call.answer('Сейчас будет отправлен скриншот отчета')
    file_type = call.data.split('_')[0]
    file_id = call.data.split('_')[1]

    #await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.edit_message_text('Отправляем скриншот отчета...',  chat_id=call.message.chat.id, message_id=call.message.message_id)

    #await bot.delete_message(call.message.chat.id, call.message.message_id+1) if file_type == 'report' else await bot.delete_message(call.message.chat.id, call.message.message_id-1)
    #await bot.send_message(call.message.chat.id, 'Отправляем скриншот отчета...')

    async with state.proxy() as data:
        data['file_type'] = file_type
        data['file_id'] = file_id
        data['html'] = await screenshot.create_page(call.message.chat.id, {'docID': file_id, 'docType': file_type})
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('test.png'))
    if file_type == 'document':
        yes_no_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data=f'addFilter'),
                                                     InlineKeyboardButton('Нет', callback_data='NoFilter'))
        await bot.send_message(call.message.chat.id, 'Хотите добавить фильтр на отчет?', reply_markup=yes_no_keyboard)
    else:
        await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
        await state.finish()


@dp.callback_query_handler(Text(startswith='NoFilter'), state=get_info.file_data)
async def no_filter(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()


@dp.callback_query_handler(Text(startswith='addFilter'), state=get_info.file_data)
async def get_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    async with state.proxy() as data:
        data['all_selectors'] = await screenshot.get_selectors(call.message.chat.id)
        data['active_selectors'] = await screenshot.get_selectors(call.message.chat.id)
        data['final'] = {}

    if data['file_type'] == 'document':
        selectors_keyboard = InlineKeyboardMarkup()
        for selector_name in data['active_selectors'].keys():
            #print('selector_'+selector_name + '_' + data['active_selectors'][selector_name])
            if selector_name[0] not in ('S', 's'):
                selectors_keyboard.add(InlineKeyboardButton(selector_name, callback_data='sel,'+selector_name + ',' + data['active_selectors'][selector_name]))
        selectors_keyboard.add(InlineKeyboardButton('Продолжить', callback_data='continue'))
        await bot.send_message(call.message.chat.id, 'Выберите селекторы на которые хотите добавить фильтр', reply_markup=selectors_keyboard)


@dp.callback_query_handler(Text(startswith='sel,'), state=get_info.file_data)
async def add_selector(call: aio.types.CallbackQuery, state: FSMContext):
    selector_name = call.data.split(',')[1]
    ckey = call.data.split(',')[2]
    new_keyboard = InlineKeyboardMarkup()

    await bot.send_message(call.message.chat.id, f'Выбран селектор {selector_name}')

    async with state.proxy() as data:
        data[f'values,{selector_name},{ckey}'] = await screenshot.get_values(call.message.chat.id, ckey)
        data['active_selectors'].pop(selector_name)
    for s_name in data['active_selectors'].keys():
        if s_name[0] not in ('s', 'S'):
            new_keyboard.add(InlineKeyboardButton(s_name, callback_data='sel,'+s_name + ',' + data['active_selectors'][s_name]))
    new_keyboard.add(InlineKeyboardButton('Продолжить', callback_data='continue'))
    await bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id, reply_markup=new_keyboard)


@dp.callback_query_handler(Text(equals='continue'), state=get_info.file_data)
async def add_values(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        for selector in data.keys():
            if selector.startswith('values'):
                values_keyboard = InlineKeyboardMarkup(row_width=2)
                #print(data[selector].keys())
                c = 0
                for key in data[selector]:
                    if c <= 50:
                        values_keyboard.insert(InlineKeyboardButton(key, callback_data='add,' + selector.split(',')[1] + ',' + data[selector][key]))
                    else:
                        break
                    c += 1
                await bot.send_message(call.message.chat.id, 'Выберите значение селектора ' + selector.split(',')[1] + ':', reply_markup=values_keyboard)
    await bot.send_message(call.message.chat.id, 'После выбора нужных селекторов нажмите \'Продолжить\':', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжить', callback_data='continue2')))


@dp.callback_query_handler(Text(startswith='add,'), state=get_info.file_data)
async def final_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()


    selector_id = call.data.split(',')[1]
    value_id = call.data.split(',')[2]
    async with state.proxy() as data:
        data['final'].update({data['all_selectors'][selector_id]: value_id})

    selector_ident = ''
    for key in data['final']:
        if data['final'][key] == value_id:
            selector_ident = key

    value_name = ''
    for key in data[f"values,{selector_id},{selector_ident}"]:
        if data[f"values,{selector_id},{selector_ident}"][key] == value_id:
            value_name = key

    await bot.send_message(call.message.chat.id, f"Селектор \'{selector_id}\': {value_name}")


        #print(data)
    #print(data['final'])


@dp.callback_query_handler(Text(equals='continue2'), state=get_info.file_data)
async def screen_with_filters(call: aio.types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    selectors = '&evt=' + '1024001' + '&src=mstrWeb.' + 'oivm.rwb.1024001' + '&events=-'
    async with state.proxy() as data:
        for ctlKey in data['final'].keys():
            selectors += f"2048084*.mstrWeb***.oivm***.rwb***.2048084*.ctlKey*.{ctlKey}*.elemList*.{data['final'][ctlKey]}*.usePartDisplay*.1*.currentIncludeState*.true*.applyNow*.0*.targetType*.0."
    selectors += '2048014*.mstrWeb***.oivm***.rwb***.2048014_&evtorder=2048001%2c1024001&2048001=1&1024001=1'
    #await screenshot.screenshot_html({'docID': data['file_id'], 'docType': data['file_type']}, selectors)
    #await screenshot.create_page({'browser': browser,'user_id':call.message.chat.id, 'docID': file_id, 'docType': file_type})
    await bot.send_photo(chat_id=call.message.chat.id, photo=InputFile('test.png'), caption='Скриншот с добавленными фильтрами')
    await bot.send_message(call.message.chat.id, 'Введите /search для поиска отчетов')
    await state.finish()



aio.executor.start_polling(dp, on_startup=on_startup)