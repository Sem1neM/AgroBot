import datetime
import time

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, document
from aiogram.filters import Command, StateFilter

from config import last_request_time, MAX_REQUESTS_PER_SECOND, navigation_map_path, DOCUMENT_PATH
from kb import make_row_keyboard, make_column_keyboard
from models.models import Feedback
from states import States, FeedbackState
from texts import *

router = Router()


# Команда start
@router.message(StateFilter(None), Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply(
        START_TEXT, reply_markup=make_column_keyboard(START_KB)
    )
    await state.set_state(States.FIRST_CHOICE)


# Обработка сообщений с цифрами (категории деятельности
# TODO: Переделать дорожную карту, придумать алгоритм обработки подбора финансирования
@router.message(States.FIRST_CHOICE)
async def send_category_info(message: types.Message, state: FSMContext):
    # Проверяем выбранную команду
    if message.text == '/cancel':
        await state.clear()
        await message.reply(CANCEL, reply_markup=types.ReplyKeyboardRemove())
        return
    category = message.text

    response = "Информация по выбранной категории:"

    if category == "Самозанятый":
        response += " Самозанятый..."
        await message.reply(response)
        await state.set_state(States.FIRST_CHOICE)

    elif category == "Личное подсобное хозяйство":
        response += " Личное подсобное хозяйство..."
        await message.reply(response)
        await state.set_state(States.FIRST_CHOICE)

    elif category == "Индивидуальный предприниматель":
        response += CHOOSE_DURATION
        await message.reply(response, reply_markup=make_row_keyboard(DURATION_KB))
        await state.set_state(States.SECOND_CHOICE)

    elif category == "ИП или Глава КФХ":
        response += CHOOSE_DURATION
        await message.reply(response, reply_markup=make_row_keyboard(DURATION_KB))
        await state.set_state(States.SECOND_CHOICE)

    elif category == "Юридическое лицо или кооператив":
        response += " Юридическое лицо или кооператив..."
        await message.reply(response)
        await state.set_state(States.FIRST_CHOICE)

    else:
        response = WRONG_CATEGORY
        await message.reply(response, reply_markup=make_column_keyboard(START_KB))
        await state.set_state(States.FIRST_CHOICE)

    # Обработчик выбора ответа


# TODO: Переделать под дорожную карту
@router.message(lambda message: message.text in DURATION_KB, States.SECOND_CHOICE)
async def handle_choice(message: types.Message, state: FSMContext):
    if message.text == '/cancel':
        await state.clear()
        await message.reply(CANCEL, reply_markup=types.ReplyKeyboardRemove())
        return
    # Отправляем сообщение с выбранным вариантом ответа
    await message.answer(f"Вы выбрали: {message.text}", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


# Команда help
@router.message(Command("help"))
async def send_help(message: types.Message):
    await message.reply(COMMANDS)
    print(message.chat.id)


# Команда navigation_map
@router.message(Command("navigation_map"))
async def send_navigation_map(message: types.Message):
    navigation_map = FSInputFile(navigation_map_path)
    await message.answer_photo(navigation_map, caption=NAVIGATION_MAP)


# Команда info
@router.message(Command("about"))
async def send_info(message: types.Message):
    await message.reply(INFO)


# Команда contact
@router.message(Command("contact"))
async def send_contact_info(message: types.Message):
    await message.reply(CONTACT)


# Команда feedback
@router.message(Command("feedback"))
async def request_feedback(message: types.Message, state: FSMContext):
    await message.reply(FEEDBACK)
    # Перевод бота в режим ожидания обратной связи
    await state.set_state(FeedbackState.WaitingForFeedback)


# Обработчик команды /cancel
@router.message(Command("cancel"), FeedbackState.WaitingForFeedback)
async def cancel_feedback_command(message: types.Message, state: FSMContext):
    await message.answer(FEEDBACK_CANCEL)
    # Сбрасываем состояние обратной связи
    await state.clear()


@router.message(Command("vika"))
async def cancel_feedback_command(message: types.Message):
    await message.answer(VIKA)


@router.message(Command("egor"))
async def cancel_feedback_command(message: types.Message):
    await message.answer(EGOR)


# Обработчик для всех остальных сообщений
@router.message(FeedbackState.WaitingForFeedback)
async def handle_feedback_message(message: types.Message, state: FSMContext):
    try:
        # Сохранение сообщения обратной связи в базе данных
        Feedback(user_id=message.from_user.username, message=message.text, message_time=datetime.datetime.now()).save()
        # Подтверждение получения обратной связи пользователю
        await message.answer(FEEDBACK_THANKS)

    except:
        await message.answer(FEEDBACK_ERROR)

    finally:
        # Возвращение бота в начальное состояние
        await state.clear()

@router.message(Command("document"))
async def document_command(message: types.Message):
    doc = FSInputFile(DOCUMENT_PATH)
    await message.reply_document(doc, caption=DOCUMENT)


# Обработчик для всех остальных сообщений
@router.message()
async def handle_unknown(message: types.Message):
    user_id = message.from_user.id

    # Получаем текущее время
    current_time = time.time()

    # Проверяем, прошло ли достаточно времени с момента последнего запроса от этого пользователя
    if user_id in last_request_time and current_time - last_request_time[user_id] < 1 / MAX_REQUESTS_PER_SECOND:
        await message.answer(WAIT_SPAM)
        return

    await message.answer(UNKNOWN_COMMAND)

    # Обновляем время последнего запроса от пользователя
    last_request_time[user_id] = current_time
