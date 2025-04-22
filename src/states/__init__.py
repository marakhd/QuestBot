from aiogram.fsm.state import State, StatesGroup


class QuestState(StatesGroup):
    answer = State()


class AdditionalTask(StatesGroup):
    download_video = State()

class PrimarySchoolState(StatesGroup):
    answer = State()
