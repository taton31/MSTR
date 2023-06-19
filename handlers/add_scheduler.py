
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, db, bot, conn

from webdriver.scheduler import scheduler, get_user_jobs

from mstr_connect import get_document_name_by_id

from translate import _


# Функция добавления подписки
async def add_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    time_or_trigger_keyboard = InlineKeyboardMarkup(row_width=2)
    time_or_trigger_keyboard.insert(InlineKeyboardButton(_(User.get_current().id)('time_scheduler'), callback_data=f'add_time_sch'))
    time_or_trigger_keyboard.insert(InlineKeyboardButton(_(User.get_current().id)('trigger_scheduler'), callback_data=f'add_trigger_sch'))
    await bot.send_message(User.get_current().id, _(User.get_current().id)('set_type_of_scheduler'), reply_markup=time_or_trigger_keyboard)


async def list_of_time_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await state.reset_state(with_data=False)
    all_subscription = get_user_jobs(str(User.get_current().id))
    all_subscription_keyboard = InlineKeyboardMarkup()
    if all_subscription:
        for job in all_subscription:
            all_subscription_keyboard.add(InlineKeyboardButton(text=get_document_name_by_id(conn, job.name), callback_data=f'info_about_time_sch:{job.id}'))
        await bot.send_message(User.get_current().id, _(User.get_current().id)('list_of_scheduler'), reply_markup=all_subscription_keyboard)
    else:
        await bot.send_message(User.get_current().id, _(User.get_current().id)('list_of_scheduler_is_empty'))

        
async def list_of_trigger_scheduler(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await state.reset_state(with_data=False)
    all_subscription = db.get_user_triggers(str(User.get_current().id))
    all_subscription_keyboard = InlineKeyboardMarkup()
    if all_subscription:
        for subscription in all_subscription.keys():
            all_subscription_keyboard.add(InlineKeyboardButton(text=all_subscription[subscription], callback_data=f'info_about_trigger_sch:{subscription}'))
        await bot.send_message(User.get_current().id, _(User.get_current().id)('list_of_scheduler'), reply_markup=all_subscription_keyboard)
    else:
        await bot.send_message(User.get_current().id, _(User.get_current().id)('list_of_scheduler_is_empty'))

def register_handlers_search_and_screen(dp: Dispatcher):
    dp.register_callback_query_handler(add_scheduler, Text(equals='add_scheduler'), state=GetInfo.set_filters)
    dp.register_callback_query_handler(list_of_time_scheduler, Text(equals='list_of_time_scheduler'), state='*')
    dp.register_callback_query_handler(list_of_trigger_scheduler, Text(equals='list_of_trigger_scheduler'), state='*')
