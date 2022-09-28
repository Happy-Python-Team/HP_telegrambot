from aiogram import types, Dispatcher

from bot_configure import bot
from keyboards.support_keyboard import kb_donate
from keyboards.vk_parser_keyboard import kb_client


async def support(message: types.Message):
    await bot.send_message(message.from_user.id, "Несколько способов поддержать нас", reply_markup=kb_donate)
    await bot.send_message(message.from_user.id, "Продолжайте работу", reply_markup=kb_client)


def register_handlers_support(dp: Dispatcher):
    dp.register_message_handler(support)