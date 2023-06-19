from create_bot_and_conn import dp
from aiogram import executor
from handlers import (commands, find_another_report, language, no_filter, screen_with_filters,
                      search_and_screen, set_selectors, add_favorite, add_scheduler, add_time_scheduler, add_trigger_scheduler, screen_favorite)

# Регистрируем хэндлеры
commands.register_handlers_commands(dp)
language.register_handlers_language(dp)
search_and_screen.register_handlers_search_and_screen(dp)
screen_favorite.register_handlers_screen_with_filters(dp)
add_favorite.register_handlers_search_and_screen(dp)
add_scheduler.register_handlers_search_and_screen(dp)
add_time_scheduler.register_handlers_search_and_screen(dp)
add_trigger_scheduler.register_handlers_search_and_screen(dp)
no_filter.register_handlers_no_filters(dp)
set_selectors.register_handlers_set_selectors(dp)
screen_with_filters.register_handlers_screen_with_filters(dp)
find_another_report.register_handlers_find_another_report(dp)

# Запускаем поллинг
executor.start_polling(dp)


# TODO Добавить ссылку на сам отчет в боте
# TODO поиск по значению для селектора
# TODO не тянуть имена для избранного и подписок из мстр апи
# TODO несколько подписок (избранного) на один документ
# TODO Логирование
# TODO Подписка (мстровская) не приходит, пока не пинганешь разок


