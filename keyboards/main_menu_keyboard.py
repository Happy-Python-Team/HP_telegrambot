from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_configure import config


b1 = KeyboardButton(config.get('RUSSIAN', 'parse_group'))
b2 = KeyboardButton(config.get('RUSSIAN', 'donate_btn_text'))
b3 = KeyboardButton(config.get('RUSSIAN', 'stop_work'))
b5 = KeyboardButton(config.get('RUSSIAN','analizing'))
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_client.row(b1,b5).add(b2).add(b3)
