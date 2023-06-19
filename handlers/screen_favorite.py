
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot_and_conn import db, GetInfo, bot

from webdriver.scheduler import send_filter_screen, create_page

from translate import _

from log.create_loggers import bot_logger


# Функция отправки скриншота отчета из избранного
async def get_screen_favorite(call: CallbackQuery, state: FSMContext):
    await bot.send_message(call.message.chat.id, _(call.message.chat.id)('send_favorite'))
    all_favorites = db.get_favorite(User.get_current().id)
    file_id = call.data.split(':')[1]
    await create_page(User.get_current().id, {'docID': file_id})
    try:
            await send_filter_screen(User.get_current().id, {'filters': all_favorites[file_id], 'security': db.get_security(User.get_current().id)}, is_ctlkey=False)
    except KeyError as e:
        if e.args[0] == 'S_security':
            await bot.send_message(call.message.chat.id, _(call.message.chat.id)('security_key_error'))
            await bot.send_message(call.message.chat.id, _(call.message.chat.id)('file_name'))
            await GetInfo.find_file.set()
            return
    except TimeoutError as e:
        if e.args[0] == 'Session is dead':
            await bot.send_message(call.message.chat.id, _(call.message.chat.id)('session_is_dead'))
            await bot.send_message(call.message.chat.id, _(call.message.chat.id)('file_name'))
            await GetInfo.find_file.set()
            return
    except:
        bot_logger.exception(f'\tuser_ID:{call.message.chat.id}')
    yes_no_keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(_(call.message.chat.id)('yes'), callback_data='yesFilter')
    no_button = InlineKeyboardButton(_(call.message.chat.id)('no'), callback_data='noFilter')
    yes_no_keyboard.add(yes_button, no_button)
    await bot.send_message(call.message.chat.id, _(call.message.chat.id)('add_filter'), reply_markup=yes_no_keyboard)
    await GetInfo.set_filters.set()


def register_handlers_screen_with_filters(dp: Dispatcher):
    dp.register_callback_query_handler(get_screen_favorite, Text(startswith='fav:'), state="*")
