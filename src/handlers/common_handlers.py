from aiogram import Router, Bot, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.types import ChatMemberUpdated, Chat, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, Command, StateFilter
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.filters.chat_member_updated import IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.lexicon import lexicon_ru
from src.keyboards import keyboards_ru
from src.callbacks.callback_data import UserRole
from src.database import functions


router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(text=lexicon_ru.START_MESSAGE,
                         reply_markup=keyboards_ru.get_role_keyboard(show_how_it_works=True))


@router.callback_query(F.data == 'how_it_works')
async def process_how_it_works(callback: CallbackQuery):
    await callback.message.edit_text(text=lexicon_ru.HOW_IT_WORKS_TEXT,
                                     reply_markup=keyboards_ru.get_role_keyboard(show_how_it_works=False))


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=lexicon_ru.HELP_TEXT)
