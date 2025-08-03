from aiogram import Router, Bot, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ChatMemberUpdated, Chat, CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, Command, StateFilter

from src.callbacks.callback_data import UserName, UserRole, RegionCallback, CategoriesCallback
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
async def process_user_region(callback: CallbackQuery, state: FSMContext):
    selected_categories = set()
    await state.update_data(selected_categories=selected_categories)
    await callback.message.edit_text(text=lexicon_ru.PROFILE_CATEGORIES_PROMPT,
                                     reply_markup=keyboards_ru.get_or_update_categories_keyboard(selected_categories))


@router.callback_query(CategoriesCallback.filter())
async def process_user_category(callback: CallbackQuery, state: FSMContext, callback_data: CategoriesCallback):
    data = await state.get_data()
    selected_categories: set = data.get('selected_categories', set())
    if callback_data.categories not in selected_categories:
        selected_categories.add(callback_data.categories)
    else:
        selected_categories.remove(callback_data.categories)
    await callback.message.edit_text(
        text=lexicon_ru.PROFILE_CATEGORIES_PROMPT,
        reply_markup=keyboards_ru.get_or_update_categories_keyboard(selected=selected_categories)
    )
    await state.update_data(selected_categories=selected_categories)


@router.callback_query(F.data == 'ok')
async def process_profile_created(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    categ = data.get('selected_categories')
    if categ:
        await callback.message.edit_text(text=lexicon_ru.PROFILE_CREATED_SUCCESS)
        # ТЕСТ для меню
        await callback.message.answer(text='Твое меню')
    else:
        await callback.answer(text="Выберете хотя бы одну категорию, чтобы продолжить.")
