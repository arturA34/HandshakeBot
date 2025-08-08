from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.callbacks.callback_data import CategoriesCallback
from src.keyboards import keyboards_ru
from src.lexicon import lexicon_ru


async def update_category(state: FSMContext, callback_data: CategoriesCallback) -> set:
    data = await state.get_data()
    selected_categories: set = data.get('selected_categories', set())
    if callback_data.categories not in selected_categories:
        selected_categories.add(callback_data.categories)
    else:
        selected_categories.discard(callback_data.categories)
    return selected_categories


async def process_username_common(state: FSMContext, name: str, message: Message|CallbackQuery):
    await state.update_data(name=name)
    if isinstance(message, Message):
        await message.answer(text=lexicon_ru.PROFILE_LOCATION_PROMPT,
                             reply_markup=keyboards_ru.get_location_keyboard())
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(text=lexicon_ru.PROFILE_LOCATION_PROMPT,
                                        reply_markup=keyboards_ru.get_location_keyboard())


async def get_selected_categories(state: FSMContext):
    data = await state.get_data()
    categories: set = data.get('selected_categories')
    return categories, data
