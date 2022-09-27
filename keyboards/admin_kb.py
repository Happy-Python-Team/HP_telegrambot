from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot_configure import config


# Кнопки действий
action_b1 = KeyboardButton(config.get('RUSSIAN', 'admin_b1_text'))
action_b2 = KeyboardButton(config.get('RUSSIAN', 'admin_b2_text'))

delete_button = InlineKeyboardButton('Удалить', callback_data='delete')

kb_action = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_action.row(action_b1, action_b2)

kb_inline_del = InlineKeyboardMarkup()
kb_inline_del.add(delete_button)
