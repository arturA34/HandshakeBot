from aiogram.fsm.state import StatesGroup, State


class ExecutorRegistration(StatesGroup):
    wait_name = State()
    wait_location = State()
    wait_category = State()
