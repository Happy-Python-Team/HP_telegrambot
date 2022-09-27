from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot_configure import config

button_donate = InlineKeyboardButton('Перевод с карты', url="http://surl.li/ayyaj")
bot_link = InlineKeyboardButton('Подписаться на ВК', url="https://vk.com/happython")
bot_ds = InlineKeyboardButton('Связь с разработчиками Discord', url="https://discord.gg/XEWjcZQZ5Y")
bot_telegram = InlineKeyboardButton('Общий чат Telegram', url="https://t.me/+C03fbNGA9yI2OWIy")

kb_donate = InlineKeyboardMarkup()
kb_donate.add(button_donate).add(bot_link).add(bot_ds).add(bot_telegram)
