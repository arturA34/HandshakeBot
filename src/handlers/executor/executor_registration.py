from aiogram import Router, Bot, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ChatMemberUpdated, Chat, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, Command, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from src.callbacks.callback_data import UserName, UserRole, RegionCallback, CategoriesCallback, AcceptingCallback
from src.lexicon import lexicon_ru
from src.keyboards import keyboards_ru
from src.states import registration_states
from src.utils import executor_utils
from src.database import functions

from src.handlers.executor.executor_handlers import show_executor_menu

router = Router()


@router.callback_query(UserRole.filter(F.role == 'executor'))
async def process_user_role(callback: CallbackQuery, state: FSMContext):
    await state.set_state(registration_states.ExecutorRegistration.wait_name)
    await callback.message.edit_text(text=lexicon_ru.NEW_EXECUTOR_TEXT,
                                     reply_markup=keyboards_ru.get_new_users_keyboard(name=callback.from_user.first_name))


@router.message(StateFilter(registration_states.ExecutorRegistration.wait_name))
async def process_user_name_by_message(message: Message, state: FSMContext):
    await executor_utils.process_username_common(state=state, message=message, name=message.text)
    await state.set_state(registration_states.ExecutorRegistration.wait_location)


@router.callback_query(UserName.filter(), StateFilter(registration_states.ExecutorRegistration.wait_name))
async def process_user_name(callback: CallbackQuery, state: FSMContext, callback_data: UserName):
    await executor_utils.process_username_common(state=state, message=callback, name=callback_data.name)
    await state.set_state(registration_states.ExecutorRegistration.wait_location)


@router.callback_query(RegionCallback.filter(), StateFilter(registration_states.ExecutorRegistration.wait_location))
async def process_user_region(callback: CallbackQuery, state: FSMContext, callback_data: RegionCallback):
    await state.set_state(registration_states.ExecutorRegistration.wait_category)
    await state.update_data(location=callback_data.region)
    selected_categories = set()
    await state.update_data(selected_categories=selected_categories)
    await callback.message.edit_text(text=lexicon_ru.PROFILE_CATEGORIES_PROMPT,
                                     reply_markup=keyboards_ru.get_or_update_categories_keyboard(selected_categories))


@router.callback_query(CategoriesCallback.filter(), StateFilter(registration_states.ExecutorRegistration.wait_category))
async def process_user_category(callback: CallbackQuery, state: FSMContext, callback_data: CategoriesCallback):
    selected_categories = await executor_utils.update_category(state=state, callback_data=callback_data)
    await callback.message.edit_text(
        text=lexicon_ru.PROFILE_CATEGORIES_PROMPT,
        reply_markup=keyboards_ru.get_or_update_categories_keyboard(selected=selected_categories)
    )
    await state.update_data(selected_categories=selected_categories)


@router.callback_query(AcceptingCallback.filter(), StateFilter(registration_states.ExecutorRegistration.wait_category))
async def process_profile_created(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    categ: set = data.get('selected_categories')
    if categ:
        await functions.add_new_executor(user_id=callback.from_user.id, data=data, db=session)
        await callback.message.edit_text(text=lexicon_ru.PROFILE_CREATED_SUCCESS)
        await show_executor_menu(message=callback.message)
        await state.clear()
    else:
        await callback.answer(text="Выберете хотя бы одну категорию, чтобы продолжить.")
