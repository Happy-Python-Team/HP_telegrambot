from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot_configure import config


# Кнопки действий
action_b1 = KeyboardButton(config.get('RUSSIAN', 'admin_b1_text'))
action_b2 = KeyboardButton(config.get('RUSSIAN', 'admin_b2_text'))



kb_action = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_action.row(action_b1, action_b2)


