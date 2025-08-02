from aiogram.fsm.state import StatesGroup, State


class ExecutorRegistration(StatesGroup):
    wait_name = State()