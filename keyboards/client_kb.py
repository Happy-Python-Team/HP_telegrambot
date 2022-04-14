from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_configure import config

config.get('RUSSIAN', 'client_b1_text')
b2 = KeyboardButton(config.get('RUSSIAN', 'client_b3_text'))
b3 = KeyboardButton(config.get('RUSSIAN', 'client_b1_text'))
b4 = KeyboardButton(config.get('RUSSIAN', 'client_b2_text'))
b5 = KeyboardButton(config.get('RUSSIAN', 'donate_btn_text'))
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b4).add(b5).add(b2)
