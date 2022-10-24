from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from bot_configure import bot
from bot_configure import config
from scripts import parser_script
from keyboards import kb_client, kb_action


# Это класс машины состояний, то есь поля которые нужно вводить пользователю
class FSMAdmin(StatesGroup):
    group_name = State()
    post_count = State()
    user_shortname = State()
    action = State()


async def command_start(message: types.Message):
    try:

        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'hello_message'), reply_markup=kb_client)
        await message.delete()
    except Exception:
        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'except_message'))


# Это функция начала ввода она вызывается по команде /start ( указано внизу при регистрации Хэндлера)
async def cm_start(message: types.Message):
    await FSMAdmin.group_name.set()  # отсюда перекидывает в функцию
    await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'vk_domen'))


async def group_name(message: types.Message, state: FSMContext):
    if message.text == config.get('RUSSIAN', 'stop_work'):
        await stop_work(message)
        await command_start(message)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['group_name'] = message.text
            data['tg_id'] = message.from_user.id
        await FSMAdmin.user_shortname.set()  # перекидывает на следующую функцию, в порядке состояний в классе FSMAdmin
        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'vk_username'))


async def short_username(message: types.Message, state: FSMContext):
    if message.text == config.get('RUSSIAN', 'stop_work'):
        await stop_work(message)
        await command_start(message)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['short_username'] = message.text
        await FSMAdmin.post_count.set()
        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'post_count'))


async def post_count(message: types.Message, state: FSMContext):
    if message.text == config.get('RUSSIAN', 'stop_work'):
        await stop_work(message)
        await command_start(message)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['post_count'] = message.text

        await FSMAdmin.action.set()
        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'get_action'), reply_markup=kb_action)


async def action_user(message: types.Message, state: FSMContext):
    if message.text == config.get('RUSSIAN', 'send'):

        await bot.send_message(message.from_user.id, '✅ Запрос отправлен! Ожидайте ответа')

        await parser_script.sql_read(message=message, state=state)

        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'back_to_menu'), reply_markup=kb_client)
        await state.finish()
    else:
        await state.finish()  # Убивает машину состояний, обязательно иначе кнопки не обновятся
        await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'back_to_menu'), reply_markup=kb_client)


async def stop_work(message: types.Message):
    await bot.send_message(message.from_user.id, config.get('RUSSIAN', 'exit_msg'), reply_markup=ReplyKeyboardRemove())


# Регистрация всех хэндлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start',
                                                         'help'])  # Пример зарегистрированного хэндлера здесь указывают команды.
    dp.register_message_handler(cm_start, Text(equals=config.get('RUSSIAN', 'parse_group'), ignore_case=True),
                                state=None)  # здесь должна стартовать машина состояний
    dp.register_message_handler(group_name, content_types=['text'],
                                state=FSMAdmin.group_name)  # content_types не обязателен
    dp.register_message_handler(short_username, content_types=['text'],
                                state=FSMAdmin.user_shortname)  # content_types не обязателен

    dp.register_message_handler(post_count, state=FSMAdmin.post_count)

    dp.register_message_handler(action_user, state=FSMAdmin.action)
    dp.register_message_handler(stop_work, Text(equals=config.get('RUSSIAN', 'stop_work'), ignore_case=True))
