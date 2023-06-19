
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import bot, GetInfo

from webdriver.scheduler import close_browser

from translate import _


# Функция, срабатывающая при нажатии на кнопку "Найти другой отчет"
async def find_another_report(call: CallbackQuery, state: FSMContext):
    await close_browser(User.get_current().id)
    await state.reset_state(with_data=False)
    await bot.send_message(call.message.chat.id, _(call.message.chat.id)('type_search'))


def register_handlers_find_another_report(dp: Dispatcher):
    dp.register_callback_query_handler(find_another_report, Text(equals='findAnother'), state=GetInfo.set_filters)
