from aiogram.fsm.state import State, StatesGroup


class Quest(StatesGroup):
    answer = State()


class AdditionalTask(StatesGroup):
    download_video = State()
    
