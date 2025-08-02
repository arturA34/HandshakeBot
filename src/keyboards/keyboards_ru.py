from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.lexicon import lexicon_ru
from src.callbacks.callback_data import UserRole, UserName, RegionCallback
from src.lexicon.lexicon_ru import REGIONS


def get_role_keyboard(show_how_it_works: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=lexicon_ru.CUSTOMER_BTN, callback_data=UserRole(role='customer').pack()),
                InlineKeyboardButton(text=lexicon_ru.EXECUTOR_BTN, callback_data=UserRole(role='executor').pack()))
    if show_how_it_works is True:
        builder.row(InlineKeyboardButton(text=lexicon_ru.HOW_IT_WORKS_BTN, callback_data='how_it_works'))

    return builder.as_markup()


def get_users_keyboard(user_role: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if user_role == "executor":
        builder.row(InlineKeyboardButton(text=lexicon_ru.CREATE_TASK_BTN, callback_data='create_task'),
                    InlineKeyboardButton(text=lexicon_ru.MY_TASKS_BTN, callback_data='my_tasks'))

    elif user_role == "executor":
        builder.row(InlineKeyboardButton(text=lexicon_ru.FIND_TASKS_BTN, callback_data='find_tasks'),
                    InlineKeyboardButton(text=lexicon_ru.MY_RESPONSES_BTN, callback_data='my_responses'))

    return builder.as_markup()


# Клавиатура для регистрации нового пользователя.
def get_new_users_keyboard(name: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=name, callback_data=UserName(name=name).pack()))
    return builder.as_markup()


def get_location_keyboard():
    builder = InlineKeyboardBuilder()
    for region in REGIONS:
        builder.row(InlineKeyboardButton(text=region,
                                         callback_data=RegionCallback(region=region).pack()))
    return builder.as_markup()