from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot_configure import config


btn_today = KeyboardButton(config.get('RUSSIAN', 'yandex_today'))
btn_yesterday = KeyboardButton(config.get('RUSSIAN', 'yandex_yesterday'))

btn_this_mouth = KeyboardButton(config.get('RUSSIAN', 'yandex_this_mouth'))
btn_last_mouth = KeyboardButton(config.get('RUSSIAN', 'yandex_last_mouth'))

btn_period = KeyboardButton(config.get('RUSSIAN', 'yandex_period'))
btn_balance = KeyboardButton(config.get('RUSSIAN', 'btn_balance'))
btn_back = KeyboardButton(config.get('RUSSIAN', 'yandex_back'))

keyboard_yandex = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_yandex.row(btn_yesterday, btn_today).row(btn_last_mouth, btn_this_mouth).row(btn_period, btn_balance).row(btn_back)
