from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.types import ChatMemberUpdated, Chat, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, Command, StateFilter
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session


from src.lexicon import lexicon_ru
from src.keyboards import keyboards_ru
from src.callbacks import callback_data

router = Router()

# router.message.filter()


@router.message(Command(commands='start'))
async def show_executor_menu(message: Message):
    await message.answer(text=lexicon_ru.EXECUTOR_MENU_TEXT,
                         reply_markup=keyboards_ru.get_executor_menu_keyboard())


@router.callback_query(callback_data.ExecutorMenuCallback.filter())
async def process_executor_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text(text=lexicon_ru.SEARCHING_FOR_TASKS)