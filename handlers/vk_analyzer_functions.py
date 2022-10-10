from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from bot_configure import bot
from bot_configure import config
from handlers import parser_script
from handlers import vk_analyzer_script


class Vk_analysis(StatesGroup):
    command1 = State()


async def state_activate_analysis(message: types.Message):
    await message.answer('✍️Введите домен группы для анализа (название после vk.com)🔡')
    await Vk_analysis.command1.set()


async def get_analysis(message: types.Message, state: FSMContext):
    await message.answer(vk_analyzer_script.vk_analyzer_run(message))
    # завершаем состояние
    await state.finish()


# Регистрация всех хэндлеров
def register_handlers_analysis(dp: Dispatcher):
    dp.register_message_handler(state_activate_analysis, commands=['vk'], state=None),
    dp.register_message_handler(get_analysis, state=Vk_analysis.command1),

