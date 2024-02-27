from aiogram.fsm.state import StatesGroup, State


class FeedbackState(StatesGroup):
    WaitingForFeedback = State()


class States(StatesGroup):
    FIRST_CHOICE = State()
    SECOND_CHOICE = State()
