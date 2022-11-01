import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_configure import config, dp, ADMINS
from yandex.api import (parse_metrics_and_yandex_advertise_network,
                        get_balance_yandex_advertise_network)
from keyboards.main_menu_keyboard import get_main_menu
from keyboards.yandex_analyzer_keyboard import keyboard_yandex


class YandexAnalysis(StatesGroup):
    yandex = State()
    period = State()


@dp.message_handler(Text(equals=config.get('RUSSIAN', 'yandex')))
async def get_yandex(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.set_state(YandexAnalysis.yandex)
        await message.answer(text="Выберете один из вариантов", reply_markup=keyboard_yandex)
    else:
        await message.answer(text="У вас недостаточно прав для использования данной команды",
                             reply_markup=get_main_menu(message.from_user.id))


@dp.message_handler(Text(equals="Этот месяц"), state=YandexAnalysis.yandex)
async def get_yandex_this_mouth(message: types.Message):
    data_yandex_this_mouth = await parse_metrics_and_yandex_advertise_network("https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period=thismonth&dimension_field=date|day&dir=asc&entity_field=block_level")
    await message.answer(text=data_yandex_this_mouth)


@dp.message_handler(Text(equals="Прошлый месяц"), state=YandexAnalysis.yandex)
async def get_yandex_last_mouth(message: types.Message):
    data_yandex_last_mouth = await parse_metrics_and_yandex_advertise_network("https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period=lastmonth&dimension_field=date|day&dir=asc&entity_field=block_level")
    await message.answer(text=data_yandex_last_mouth)


@dp.message_handler(Text(equals="Сегодня"), state=YandexAnalysis.yandex)
async def get_yandex_today(message: types.Message):
    data_yandex_today = await parse_metrics_and_yandex_advertise_network("https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period=today&dimension_field=date|day&dir=asc&entity_field=block_level", period=False)
    await message.answer(text=data_yandex_today)


@dp.message_handler(Text(equals="Вчера"), state=YandexAnalysis.yandex)
async def get_yandex_yesterday(message: types.Message):
    data_yandex_yesterday = await parse_metrics_and_yandex_advertise_network("https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period=yesterday&dimension_field=date|day&dir=asc&entity_field=block_level", period=False)
    await message.answer(text=data_yandex_yesterday)


@dp.message_handler(Text(equals="Заданный период"), state=YandexAnalysis.yandex)
async def get_yandex_write_period(message: types.Message, state: FSMContext):
    await state.set_state(YandexAnalysis.period)
    await message.answer(text="Введите период в формате год-месяц-число:год-месяц-число")


@dp.message_handler(state=YandexAnalysis.period)
async def get_yandex_period(message: types.Message, state: FSMContext):
    periods = message.text.split(":")
    data_yandex_period = await parse_metrics_and_yandex_advertise_network(f"https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period={periods[0]}&period={periods[1]}&dimension_field=date|day&dir=asc&entity_field=block_level", btn="период")
    await state.finish()
    await message.answer(text=data_yandex_period, reply_markup=keyboard_yandex)


@dp.message_handler(Text(equals="Баланс"), state=YandexAnalysis.yandex)
async def get_balance(message: types.Message):
    url = f"https://partner2.yandex.ru/api/statistics2/get.json?lang=ru&pretty=1&field=partner_wo_nds&period=2022-10-03&period={datetime.datetime.now().date()}"
    balance = await get_balance_yandex_advertise_network(url)
    await message.answer(text=balance)


@dp.message_handler(Text(equals="Назад"), state=YandexAnalysis.yandex)
async def get_yandex_back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Главное меню", reply_markup=get_main_menu(message.from_user.id))
