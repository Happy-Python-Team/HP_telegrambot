from aiogram.utils import executor

import handlers.menu
from bot_configure import dp




# Здесь базовая функция, которая показывает сообщение при запуске бота в консоль.
async def on_startup(_):
    print('Start')



# # Регистрация хэндлера из файла clients в папке handlers.
handlers.menu.register_handlers_admin(dp)
handlers.other.register_handlers_other(dp)
# client.register_handlers_client(dp)  # dp - Диспетчер, обязательный аргумент для всех регистраций.
# admin.register_handlers_admin(dp)
# moderator_panel.register_handlers_moderator(dp)
# monetize.register_handlers_monetize(dp)
# other.register_handlers_other(dp)
# # Вызов этого метода, начинает прослушивание сервера телеграм на наличие подходящих нам событий. Трогать ненужно
executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
