from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup


button_donate = InlineKeyboardButton('Перевод с карты', url="http://surl.li/ayyaj")
VK_link = InlineKeyboardButton('Подписаться на ВК', url="https://vk.com/happython")
TG_link = InlineKeyboardButton('Наш телеграм', url="https://t.me/python_parser_learning")
site_link = InlineKeyboardButton('Наш сайт', url="https://happypython.ru")
backenddt_link = InlineKeyboardButton('Канал для Бэкенд разработчиков', url="https://t.me/backenddt")

kb_donate = InlineKeyboardMarkup()
kb_donate.add(button_donate).add(VK_link).add(TG_link).add(site_link).add(backenddt_link)
