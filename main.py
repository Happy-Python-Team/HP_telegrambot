"""
Это программное обеспечение распространяется по стандартной общественной лицензии GNU AGPL 3.0.

Разрешения по лицензии:

Коммерческое использование
Модификация
Распределение
Использование патентов
Частное использование

Условия использования:

Обязательное уведомление о текущей лицензии и авторских правах в вашей копии
Любые изменения лицензированного кода должны быть доступны в открытом виде
В вашей копии должна содержаться ссылка на источник программного продукта
Любые изменения в коде должны быть произведены под такой же лицензией

(с) Happy Python (invoice@happypython.ru)


"""
from aiogram.utils import executor

import handlers.vk_parser_functions
from bot_configure import dp


# Здесь базовая функция, которая показывает сообщение при запуске бота в консоль.
async def on_startup(_):
    print('Start')


# # Регистрация хэндлера из файла clients в папке handlers.
handlers.vk_analyzer_functions.register_handlers_analysis(dp)
handlers.vk_parser_functions.register_handlers_admin(dp)
handlers.support_functions.register_handlers_support(dp)
handlers.other_functions.register_handlers_other(dp)
executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
