from aiogram import types, Dispatcher

from bot_configure import bot
from bot_configure import config
from keyboards.main_menu_keyboard import get_main_menu


async def other_text(message: types.Message):
    await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'other_messages'), reply_markup=get_main_menu(message.from_user.id))


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(other_text)