from aiogram import Router, Bot, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ChatMemberUpdated, Chat, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, Command, StateFilter

from src.callbacks.callback_data import UserName, UserRole, RegionCallback
from src.lexicon import lexicon_ru
from src.keyboards import keyboards_ru
from src.states import registration_states

router = Router()


@router.callback_query(UserRole.filter(F.role == 'executor'))
async def process_users_role(callback: CallbackQuery, state: FSMContext):
    await state.set_state(registration_states.ExecutorRegistration.wait_name)
    await callback.message.edit_text(text=lexicon_ru.NEW_EXECUTOR_TEXT,
                                     reply_markup=keyboards_ru.get_new_users_keyboard(name=callback.from_user.first_name))


@router.callback_query(UserName.filter(), StateFilter(registration_states.ExecutorRegistration.wait_name))
async def process_user_name(callback: CallbackQuery):
    await callback.message.edit_text(text=lexicon_ru.PROFILE_LOCATION_PROMPT,
                                     reply_markup=keyboards_ru.get_location_keyboard())


@router.callback_query(RegionCallback.filter())
async def process_user_region(callback: CallbackQuery):
    await callback.message.edit_text(text=lexicon_ru.PROFILE_CATEGORIES_PROMPT)
