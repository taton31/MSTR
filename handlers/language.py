
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, BotCommand, BotCommandScopeChat
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from translate import _

from create_bot_and_conn import GetInfo, bot, db


# Запоминаем язык, выбранный пользователем
async def change_language(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    language = call.data.split(':')[1]
    
    db.insert_language(call.message.chat.id, language)
    await bot.set_my_commands([
            BotCommand("start", _(call.message.chat.id)('start_command')),
            BotCommand("language", _(call.message.chat.id)('language_command')),
            BotCommand("help", _(call.message.chat.id)('help_command')),
            BotCommand("search", _(call.message.chat.id)('search_command')),
            BotCommand("favorite", _(call.message.chat.id)('favorite_command')),
            BotCommand("delete_favorite", _(call.message.chat.id)('delete_favorite_command')),
            BotCommand("subscription", _(call.message.chat.id)('subscription_command')),
        ],
        BotCommandScopeChat(call.message.chat.id))
    
    await bot.send_message(call.message.chat.id, text=_(call.message.chat.id)('language_changed'))
    await state.reset_state(with_data=False)


def register_handlers_language(dp: Dispatcher):
    dp.register_callback_query_handler(change_language, Text(startswith='lang:'), state=GetInfo.set_language)
