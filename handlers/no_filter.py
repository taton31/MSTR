
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import GetInfo, bot

from translate import _

from webdriver.scheduler import close_browser


# Функция, срабатывающая при отказе пользователя наложить фильтры на отчет
async def no_filter(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.message.chat.id, _(call.message.chat.id)('type_search'))
    await state.reset_state(with_data=False)
    await close_browser(User.get_current().id)


def register_handlers_no_filters(dp: Dispatcher):
    dp.register_callback_query_handler(no_filter, Text(startswith='noFilter'), state=GetInfo.set_filters)