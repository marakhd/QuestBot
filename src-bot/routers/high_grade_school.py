from random import choice
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ChatAction

from tortoise.expressions import Q

from db import Class, User, Quest, Score
from config import settings
from states import HighSchoolState

router = Router()


async def generate_random_task(
    user: Class,  # , event: CallbackQuery | Message
) -> Quest | None:
    quest_type = settings.MODEL_TASKS_HIGH[user.last_task_number - 1]
    quests = await Quest.filter(
        (
            (Q(answer_type="TEXT") | Q(answer_type="CHOICE"))
            if quest_type == "TEXT"
            else Q(answer_type=quest_type)
        ),
        grade_group="5-11",
        is_active=True,
    ).all()
    
    active_quest = []
    for quest in quests:
        if not await Score.get_or_none(quest=quest, user=user):
            active_quest.append(quest)

    return choice(active_quest) if active_quest else None


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

    user, _ = await User.get_or_create(
        tg_id=callback.from_user.id,
        defaults={
            "sch_class": class_,
            "tg_username": callback.from_user.username,
            # "tg_id": callback.from_user.id,
            "full_name": callback.from_user.full_name,
            "last_task_number": 1,
        },
    )

    if not user.last_task:
        task = await generate_random_task(user)

        if task:
            user.last_task = task
            await user.save()
        else:
            callback.answer("Квест завершен! Заданий больше нет...")
            return

    kb = InlineKeyboardBuilder().button(
        text="Перейти к квесту",
        callback_data=f"quest_{user.last_task_number}_{user.last_task.id}",
    )

    await state.set_data({"user": user, "class": class_})

    await callback.answer()

    await callback.message.edit_text(
        "Выберите действие",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data.startswith("quest_"))
async def quest_high(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    state_data = await state.get_data()
    quest_number = int(data[1])
    quest_id = int(data[2]) if len(data) > 2 else None

    user: User = state_data.get(
        "user",
        await User.get(tg_id=callback.from_user.id).prefetch_related("sch_class"),
    )
    # class_: Class = state_data.get("user", user.sch_class)
    # quest_type = settings.MODEL_TASKS_HIGH[quest_number - 1]

    if quest_number == 1:
        user.start_time = datetime.now()
        await user.save()

    if quest_number > len(settings.MODEL_TASKS_HIGH):
        await callback.message.edit_text("Вы завершили квест!")
        await callback.message.answer("🎆")
        user.end_time = datetime.now()
        await user.save()
        return

    if not quest_id:
        active_quest = await generate_random_task(user)
        if not active_quest:
            await callback.answer("Квест завершен, доступных заданий не осталось")
            await callback.message.answer("🎆")
            user.end_time = datetime.now()
            await user.save()
    else:
        active_quest = await Quest.get_or_none(id=quest_id)

    if await Score.get_or_none(quest=active_quest, user=user):
        await callback.answer("Задание уже выполнено", show_alert=True)
        return

    if not active_quest:
        await callback.answer("Задание не найдено", show_alert=True)
        user.end_time = datetime.now()
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
    await state.set_data({"quest": active_quest, "quest_number": quest_number})
    
    if active_quest.answer_type == "MUSIC":
        await callback.message.delete()
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.UPLOAD_VOICE)
        await callback.message.answer_audio(
            (
                FSInputFile(settings.STATIC_DIR / active_quest.data.split("/")[1])
                if active_quest.data.startswith("static")
                else URLInputFile(active_quest.data, timeout=60)
            ),
            caption=f"""
Задание {quest_number} из {len(settings.MODEL_TASKS_HIGH)}\n\n
{active_quest.text}\n\n
""",
# Ответ: <code>{active_quest.correct_answer}</code>
            reply_markup=kb.as_markup(),
        )
    elif active_quest.answer_type == "PIC":
        await callback.message.delete()
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.UPLOAD_PHOTO)
        await callback.message.answer_photo(
            (
                FSInputFile(settings.STATIC_DIR / active_quest.data.split("/")[1])
                if active_quest.data.startswith("static")
                else URLInputFile(active_quest.data, timeout=90)
            ),
            caption=f"""
Задание {quest_number} из {len(settings.MODEL_TASKS_HIGH)}\n
{active_quest.text}\n
""",
# Ответ: <code>{active_quest.correct_answer}</code>
            reply_markup=kb.as_markup(),
        )
    else:
        await callback.bot.send_chat_action(callback.from_user.id, ChatAction.TYPING)
        try:
            await callback.message.edit_text(
                # f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
                f"""
Задание {quest_number} из {len(settings.MODEL_TASKS_HIGH)}\n
{active_quest.text}\n
""",
# Ответ: <code>{active_quest.correct_answer}</code>
                reply_markup=kb.as_markup(),
            )
        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                f"Квест №{quest_number}\n\n{active_quest.text}\n\nОтвет: {active_quest.correct_answer}",
                reply_markup=kb.as_markup(),
            )

    await callback.answer()


@router.callback_query(F.data.startswith("answer_high_"), HighSchoolState.answer)
@router.message(F.text, HighSchoolState.answer)
async def answer_high(update: CallbackQuery | Message, state: FSMContext):
    data = await state.get_data()
    quest_number = data.get("quest_number")
    quest: Quest | None = data.get("quest")
    # user: User = await User.get(tg_id=update.from_user.id)
    user: User = data.get("user", await User.get(tg_id=update.from_user.id))

    if not quest and not quest_number:
        update.answer("Ошибка", show_alert=True)
        return

    message: Message = update.message if isinstance(update, CallbackQuery) else update
    text: str = message.text if isinstance(update, Message) else update.data.replace("answer_high_", "")

    is_decided = False

    if quest.correct_answer.strip().lower().startswith(text.strip().lower()):
        if len(settings.MODEL_TASKS_HIGH) == quest_number:
            await message.answer("✅ Вы завершили квест!")
            await state.clear()
            user.end_time = datetime.now()
            await user.save()
            return
        
        is_decided = True

    await Score.create(
        quest_id=quest.id,
        user_id=user.id,
        class_=await user.sch_class.first(),
        score=1,
        is_decided=is_decided,
        answer=text,
    )

    user.last_task_number += 1
    await user.save()

    kb = InlineKeyboardBuilder().button(
        text="Следующее задание",
        callback_data=f"quest_{quest_number + 1}",
    )
    try:
        if isinstance(update, CallbackQuery):
            await message.edit_text("✅ Ответ введен!", reply_markup=kb.as_markup())
        else:
            await message.edit_text("✅ Ответ введен!", reply_markup=kb.as_markup())
    except TelegramBadRequest:
        await message.answer("✅ Ответ введен!", reply_markup=kb.as_markup())

    await state.set_data({"quest": None, "quest_number": None})

    await update.answer() if isinstance(update, CallbackQuery) else None

