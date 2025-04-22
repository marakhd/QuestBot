from aiogram.fsm.state import State, StatesGroup


class HighSchoolState(StatesGroup):
    answer = State()


class AdditionalTask(StatesGroup):
    download_video = State()

class PrimarySchoolState(StatesGroup):
    answer = State()
