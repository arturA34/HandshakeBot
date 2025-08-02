from aiogram.filters.callback_data import CallbackData


class UserRole(CallbackData, prefix='role'):
    role: str


class UserName(CallbackData, prefix='username'):
    name: str


class RegionCallback(CallbackData, prefix='region'):
    region: str
