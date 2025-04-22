from random import choice
import time

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ChatAction

from db import Class, User, Quest, Score
from config import settings
from states import HighSchoolState
import random

router = Router()


async def generate_random_task(
    user: Class,  # , event: CallbackQuery | Message
) -> Quest | None:
    quests = Quest.filter(
        grade_group="5-11",
        answer_type=settings.MODEL_TASKS_HIGH[user.last_task_number - 1],
        is_active=True,
    )

    active_quest = []
    for quest in quests:
        if not await Score.get_or_none(quest=quest, user=user):
            active_quest.append(quest)

    return choice(active_quest)


# Обработчик для выбора класса (callback)
@router.callback_query(F.data.startswith("class_"))
async def select_class(callback: CallbackQuery):
    sch_class = int(callback.data.split("_")[1])
    class_ = await Class.get(id=sch_class)

    kb = (
        InlineKeyboardBuilder()
        .button(text="Выбрать другой класс", callback_data="choice-grade_high")
        .button(text="Все верно", callback_data=f"continue_{sch_class}")
    )

    await callback.message.edit_text(
        f"Вы выбрали класс {class_.name}",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("continue_"))
async def start_quest(callback: CallbackQuery, state: FSMContext):
    sch_class = int(callback.data.split("_")[1])
    class_ = await Class.get(id=sch_class)

    user = await User.get_or_create(
        tg_id=callback.from_user.id,
        defaults={
            "sch_class": class_,
            "tg_username": callback.from_user.username,
            # "tg_id": callback.from_user.id,
            "full_name": callback.from_user.full_name,
        },
    )

    if not user.last_task:
        task = await generate_random_task(user)

        if task:
            class_.last_task = task
            await class_.save()
        else:
            callback.answer("Квест завершен! Заданий больше нет...")

    kb = InlineKeyboardBuilder().button(
        text="Перейти к квесту",
        callback_data=f"quest_{class_.last_task_number}_{class_.last_task.id}",
    )

    await state.set_data({"user": user, "class": class_})

    await callback.answer()

    await callback.message.edit_text(
        "Выберите действие",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("quest_"))
async def quest(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    state_data = await state.get_data()
    quest_number = int(data[1])
    quest_id = int(data[2]) if len(data) > 2 else None

    user: User = state_data.get(
        "user",
        await User.get(tg_id=callback.from_user.id).prefetch_related("sch_class"),
    )
    class_: Class = state_data.get("user", user.sch_class)
    quest_type = settings.model_tasks_high[quest_number - 1]

    if quest_number == 1:
        user.start_time = time.now()
        await user.save()

    if quest_number > len(settings.MODEL_TASKS_PRIMARY):
        await callback.message.edit_text("Вы завершили квест!")
        user.end_time = time.now()
        await user.save()
        return

    if not quest_id:
        active_quest = await generate_random_task(user)
        if not active_quest:
            callback.answer("Квест завершен, доступных заданий не осталось")
            user.end_time = time.now()
            await user.save()
    else:
        active_quest = await Quest.get_or_none(id=quest_id)

    if await Score.get_or_none(quest=active_quest, user=user):
        await callback.answer("Задание уже выполнено", show_alert=True)
        return

    if not active_quest:
        await callback.answer("Задание не найдено", show_alert=True)
        user.end_time = time.now()
        await user.save()
        return

    options = await active_quest.options.all()

    kb = InlineKeyboardBuilder()

    if options:
        for option in options:
            kb.button(
                text=option.option_text,
                callback_data=f"answer_high_{option.option_text}",
            )
        kb.adjust(2)

    await state.set_state(HighSchoolState.answer)
    await state.set_data({"quest": quest, "quest_number": quest_number})
    
    if quest.answer_type == "MUSIC":
        await callback.message.delete()
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.UPLOAD_VOICE)
        await callback.message.answer_audio(
            (
                FSInputFile(settings.STATIC_DIR / quest.data.split("/")[1])
                if quest.data.startswith("static")
                else URLInputFile(quest.data, timeout=60)
            ),
            caption=f"""
Задание {quest_number} из {len(settings.model_tasks_high)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.correct_answer}
""",
            reply_markup=kb.as_markup(),
        )
    elif quest.answer_type == "PIC":
        await callback.message.delete()
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.UPLOAD_PHOTO)
        await callback.message.answer_photo(
            (
                FSInputFile(settings.STATIC_DIR / quest.data.split("/")[1])
                if quest.data.startswith("static")
                else URLInputFile(quest.data, timeout=90)
            ),
            caption=f"""
Задание {quest_number} из {len(settings.model_tasks_high)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.correct_answer}
""",
            reply_markup=kb.as_markup(),
        )
    else:
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.TYPING)
        try:
            await callback.message.edit_text(
                # f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
                f"""
Задание {quest_number} из {len(settings.model_tasks_high)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.correct_answer}
""",
                reply_markup=kb.as_markup(),
            )
        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
                reply_markup=kb.as_markup(),
            )

    await callback.answer()


@router.callback_query(F.data.startswith("answer_high_"), HighSchoolState.answer)
@router.message(F.text, HighSchoolState.answer)
async def answer_primary(update: CallbackQuery | Message, state: FSMContext):
    data = await state.get_data()
    quest_number = data.get("quest_number")
    quest: Quest | None = data.get("quest")
    user: User = data.get("user", await User.get(tg_id=update.from_user.id))

    if not quest and quest_number:
        return

    message: Message = update.message if isinstance(update, CallbackQuery) else update
    text = message.text if isinstance(update, Message) else update.data

    if quest.correct_answer.lower() == text.replace("answer_primary_", "").lower():
        if len(settings.MODEL_TASKS_PRIMARY) == quest_number:
            await message.answer("✅ Вы завершили квест!")
            await state.clear()
            user.end_time = time.now()
            await user.save()
            return

        #TODO: Занести в Score

        kb = InlineKeyboardBuilder().button(
            text="Следующее задание",
            callback_data=f"quest_primary_{quest_number + 1}",
        )
        try:
            await message.edit_text("✅ Правильно!", reply_markup=kb.as_markup())
        except TelegramBadRequest:
            await message.answer("✅ Правильно!", reply_markup=kb.as_markup())

    await state.set_data({"quest": None, "quest_number": None})

    await update.answer() if isinstance(update, CallbackQuery) else None
