from aiogram.utils import executor

import handlers.menu
from bot_configure import dp




# Здесь базовая функция, которая показывает сообщение при запуске бота в консоль.
async def on_startup(_):
    print('Start')



# # Регистрация хэндлера из файла clients в папке handlers.
handlers.menu.register_handlers_admin(dp)
handlers.other.register_handlers_other(dp)
executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
