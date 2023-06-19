
import math
from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, bot, COUNT_VALUES
from webdriver.page_interaction import get_selectors

from webdriver.scheduler import get_selectors, get_values

from translate import _

from log.create_loggers import bot_logger


# Выводим список всех селекторов
async def get_all_selectors(call: CallbackQuery, state: FSMContext):

    await bot.answer_callback_query(call.id)
    await call.message.delete()

    selectors_multi, selectors_wo_multi = await get_selectors(User.get_current().id)

    # отправляем селекторы с мультивыбором
    if selectors_multi:
        selectors_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_multi:
            if selector[0] not in ('S', 's'):
                selectors_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:mult:{selector}')
                selectors_multi_keyboard.add(selectors_multi_button)
                async with state.proxy() as data:
                    data['selectors_multi'] = {**data['selectors_multi'], **{selector: selectors_multi[selector]}}
        await bot.send_message(call.message.chat.id, _(call.message.chat.id)('mult_selectors'),
                               reply_markup=selectors_multi_keyboard)

    # отправляем селекторы без мультивыбора
    if selectors_wo_multi:
        selectors_wo_multi_keyboard = InlineKeyboardMarkup()
        for selector in selectors_wo_multi:
            if selector[0] not in ('S', 's'):
                selectors_wo_multi_button = InlineKeyboardButton(selector, callback_data=f'sel:womult:{selector}')
                selectors_wo_multi_keyboard.add(selectors_wo_multi_button)
                async with state.proxy() as data:
                    data['selectors_wo_multi'] = {**data['selectors_wo_multi'], **{selector: selectors_wo_multi[selector]}}
        await bot.send_message(call.message.chat.id, _(call.message.chat.id)('wo_mult_selectors'),
                               reply_markup=selectors_wo_multi_keyboard)

    send_screen_keyboard = InlineKeyboardMarkup()
    send_screen_button = InlineKeyboardButton(_(call.message.chat.id)('get_screen'), callback_data='getScreen')
    send_screen_keyboard.add(send_screen_button)
    await bot.send_message(call.message.chat.id, _(call.message.chat.id)('get_screen'), reply_markup=send_screen_keyboard)


# Выводим список всех значений выбранного селектора
async def get_selector_values(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    selector_name = call.data.split(':')[2]
    selector_type = call.data.split(':')[1]
    selector_ctl_name = ''
    if selector_type == 'mult':
        async with state.proxy() as data:
            selector_ctl_name = data['selectors_multi'][selector_name] + f';{selector_name}'
    else:
        async with state.proxy() as data:
            selector_ctl_name = data['selectors_wo_multi'][selector_name] + f';{selector_name}'

    # добавляем ctl селектора в словарь filters
    async with state.proxy() as data:
        data['active_selector'] = selector_ctl_name
        data['filters'] = {**data['filters'], **{selector_ctl_name: []}}

    selector_values = await get_values(User.get_current().id, selector_ctl_name.split(';')[0])
    async with state.proxy() as data:
        data['selector_values'] = selector_values
        data['selector_values_keys'] = list(selector_values.keys())

    if selector_values:
        selector_values_keyboard = InlineKeyboardMarkup()
        for value in data['selector_values_keys'][0:COUNT_VALUES]:
            selector_values_button = InlineKeyboardButton(value, callback_data=f'val:{selector_type}:{value}')
            selector_values_keyboard.add(selector_values_button)

        # sliced_selector_values_keyboard = InlineKeyboardMarkup()
        # sliced_selector_values_keyboard.inline_keyboard = selector_values_keyboard.inline_keyboard[0:COUNT_VALUES]
        # AM_PM = call.message.reply_markup.inline_keyboard[0][0].text
        
        current_page = InlineKeyboardButton(_(call.message.chat.id)('current_page').format(f"1 / {math.ceil(len(data['selector_values_keys'])/COUNT_VALUES)}"), callback_data='number_of_page:0')
        previus_page = InlineKeyboardButton(_(call.message.chat.id)('previus_page'), callback_data=f'number_of_page:0')
        next_page = InlineKeyboardButton(_(call.message.chat.id)('next_page'), callback_data=f'number_of_page:2')
        selector_values_keyboard.row(previus_page, current_page, next_page)

        await bot.send_message(text=_(call.message.chat.id)('sel_val_mult' if selector_type == 'mult' else 'sel_val_wo_mult').format(selector_name),
                                        chat_id=call.message.chat.id,
                                        reply_markup=selector_values_keyboard)

        choice_keyboard = InlineKeyboardMarkup()
        choose_selector_button = InlineKeyboardButton(_(call.message.chat.id)('more_selectors'), callback_data='yesFilter')
        choose_screen_button = InlineKeyboardButton(_(call.message.chat.id)('get_screen'), callback_data='getScreen')
        choice_keyboard.add(choose_selector_button, choose_screen_button)
        await bot.send_message(chat_id=call.message.chat.id,
                               text=_(call.message.chat.id)('set_sel_val'),
                               reply_markup=choice_keyboard)


# Запоминаем выбранное значение(-я) у селектора
async def set_selector_value(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    selector_type = call.data.split(':')[1]
    selector_value_name = call.data.split(':')[2]
    selected_values = []


    async with state.proxy() as data:
        selector_name = data['active_selector'].split(';')[1]
        selector_value = data['selector_values'][selector_value_name]
        selector_ctl = data['active_selector']
        if selector_type == 'mult':
            if selector_value_name.lower() in ['all', 'все']:
                data['filters'][selector_ctl]=[{selector_value: selector_value_name}]
            elif data['filters'][selector_ctl]:
                if {selector_value: selector_value_name} not in data['filters'][selector_ctl]:
                    if list(data['filters'][selector_ctl][0].values())[0].lower() in ['all', 'все']:
                        data['filters'][selector_ctl]=[{selector_value: selector_value_name}]
                    else:
                        data['filters'][selector_ctl].append({selector_value: selector_value_name})
            else:
                data['filters'][selector_ctl]=[{selector_value: selector_value_name}]

        else:
            data['filters'][selector_ctl] = [{selector_value: selector_value_name}]
        for value_name in data['filters'][selector_ctl]:
            selected_values.append(list(value_name.values())[0])
        try:
            await call.message.edit_text(f"{_(User.get_current().id)('sel_val_mult' if selector_type == 'mult' else 'sel_val_wo_mult').format(selector_name)}\n{_(User.get_current().id)('сhosen')} {', '.join(selected_values)}",
                                        reply_markup=call.message.reply_markup)
        except MessageNotModified:
            pass
        except:
            bot_logger.exception(f'\tuser_ID:{call.message.chat.id}')


        

# переключение страниц значений селектора
async def switch_values_page(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    page_number = int(call.data.split(':')[1])
    selector_type = call.message.reply_markup.inline_keyboard[0][0].callback_data.split(':')[1]
    async with state.proxy() as data:
        if page_number < 1 or page_number > math.ceil(len(data['selector_values_keys'])/COUNT_VALUES):
            return
        call.message.reply_markup.inline_keyboard[-1][0].callback_data = f"number_of_page:{(page_number - 1)}"
        call.message.reply_markup.inline_keyboard[-1][2].callback_data = f"number_of_page:{(page_number + 1)}"
        call.message.reply_markup.inline_keyboard[-1][1].text = _(call.message.chat.id)('current_page').format(f"{page_number} / {math.ceil(len(data['selector_values_keys'])/COUNT_VALUES)}") #(page_number + 1) if page_number < math.ceil(len(data['selector_values_keys'])/COUNT_VALUES) else math.ceil(data['selector_values_keys']/COUNT_VALUES)
        if page_number < math.ceil(len(data['selector_values_keys'])/COUNT_VALUES):
            for i in range(len(call.message.reply_markup.inline_keyboard) - 1):
                call.message.reply_markup.inline_keyboard[i][0].text = data['selector_values_keys'][(page_number - 1) * COUNT_VALUES + i]
                call.message.reply_markup.inline_keyboard[i][0].callback_data = f"val:{selector_type}:{data['selector_values_keys'][(page_number - 1) * COUNT_VALUES + i]}"
        else: 
            for i in range(len(call.message.reply_markup.inline_keyboard) - 1):
                call.message.reply_markup.inline_keyboard[-i-2][0].text = data['selector_values_keys'][-i-1]
                call.message.reply_markup.inline_keyboard[-i-2][0].callback_data = f"val:{selector_type}:{data['selector_values_keys'][-i-1]}"
        try:
            await call.message.edit_reply_markup(call.message.reply_markup)
        except MessageNotModified:
            pass
        except: 
            bot_logger.exception(f'\tuser_ID:{call.message.chat.id}')




def register_handlers_set_selectors(dp: Dispatcher):
    dp.register_callback_query_handler(get_all_selectors, Text(startswith='yesFilter'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(get_selector_values, Text(startswith='sel:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(switch_values_page, Text(startswith='number_of_page:'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(set_selector_value, Text(startswith='val:'), state=GetInfo.set_filters)
