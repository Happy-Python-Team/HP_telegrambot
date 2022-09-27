from aiogram import types, Dispatcher

from bot_configure import bot
from bot_configure import config
from keyboards.support_keyboard import kb_donate


async def support(message: types.Message):
    await bot.send_message(message.from_user.id, "Несколько способов поддержать нас", reply_markup=kb_donate)


def register_handlers_support(dp: Dispatcher):
    dp.register_message_handler(support)