from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot_configure import config


btn_today = KeyboardButton(config.get('RUSSIAN', 'yandex_today'))
btn_yesterday = KeyboardButton(config.get('RUSSIAN', 'yandex_yesterday'))

btn_this_mouth = KeyboardButton(config.get('RUSSIAN', 'yandex_this_mouth'))
btn_last_mouth = KeyboardButton(config.get('RUSSIAN', 'yandex_last_mouth'))

btn_period = KeyboardButton(config.get('RUSSIAN', 'yandex_period'))
btn_back = KeyboardButton(config.get('RUSSIAN', 'yandex_back'))

keabord_yandex = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keabord_yandex.row(btn_yesterday, btn_today).row(btn_last_mouth, btn_this_mouth).row(btn_period).row(btn_back)
