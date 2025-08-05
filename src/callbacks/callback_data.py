from aiogram.filters.callback_data import CallbackData


class UserRole(CallbackData, prefix='role'):
    role: str


class UserName(CallbackData, prefix='username'):
    name: str


class RegionCallback(CallbackData, prefix='region'):
    region: str


class CategoriesCallback(CallbackData, prefix='categories'):
    categories: int


class AcceptingCallback(CallbackData, prefix='action'):
    action: str


class ExecutorMenuCallback(CallbackData, prefix='executor_menu'):
    action: str
