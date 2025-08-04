from aiogram.fsm.context import FSMContext
from src.callbacks.callback_data import CategoriesCallback


async def update_category(state: FSMContext, callback_data: CategoriesCallback) -> set:
    data = await state.get_data()
    selected_categories: set = data.get('selected_categories', set())
    if callback_data.categories not in selected_categories:
        selected_categories.add(callback_data.categories)
    else:
        selected_categories.discard(callback_data.categories)
    return selected_categories
