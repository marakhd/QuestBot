from random import choice

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, URLInputFile, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from tortoise.expressions import Q

from db import Quest
from config import settings
from states import PrimarySchoolState

# Create main router
router = Router()


@router.callback_query(F.data.startswith("quest_primary_"))
async def quest_primary(callback: CallbackQuery, state: FSMContext):
    quest_number = int(callback.data.split("_")[2])

    if quest_number > len(settings.MODEL_TASKS_PRIMARY):
        await callback.message.edit_text("Вы завершили квест!")
        return

    quest_type = settings.MODEL_TASKS_PRIMARY[quest_number - 1]

    quests = await Quest.filter(
        (
            (Q(answer_type="TEXT") | Q(answer_type="CHOICE"))
            if quest_type == "TEXT"
            else Q(answer_type=quest_type)
        ),
        grade_group="1-4",
        is_active=True,
    )

    if not quests:
        try:
            await callback.message.edit_text("Вы завершили квест!")
        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer("Вы завершили квест!")
        return

    quest = choice(list(quests))
    options = await quest.options.all()

    kb = InlineKeyboardBuilder()

    if options:
        for option in options:
            kb.button(
                text=option.option_text,
                callback_data=f"answer_primary_{option.option_text}",
            )
        kb.adjust(2)

    await state.set_state(PrimarySchoolState.answer)
    await state.set_data({"quest": quest, "quest_number": quest_number})

    if quest.answer_type == "MUSIC":
        await callback.message.delete()
        await callback.message.answer_audio(
            (
                FSInputFile(settings.STATIC_DIR / quest.data.split("/")[1])
                if quest.data.startswith("static")
                else URLInputFile(quest.data, timeout=60)
            ),
            caption=f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
            reply_markup=kb.as_markup(),
        )
    elif quest.answer_type == "PIC":
        await callback.message.delete()
        await callback.message.answer_photo(
            (
                FSInputFile(settings.STATIC_DIR / quest.data.split("/")[1])
                if quest.data.startswith("static")
                else URLInputFile(quest.data, timeout=90)
            ),
            caption=f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
            reply_markup=kb.as_markup(),
        )
    else:
        try:
            await callback.message.edit_text(
                f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
                reply_markup=kb.as_markup(),
            )
        except TelegramBadRequest:
            await callback.message.delete()
            await callback.message.answer(
                f"Квест №{quest_number}\n\n{quest.text}\n\nОтвет: {quest.correct_answer}",
                reply_markup=kb.as_markup(),
            )

    await callback.answer()


@router.callback_query(F.data.startswith("answer_primary_"), PrimarySchoolState.answer)
@router.message(F.text, PrimarySchoolState.answer)
async def answer_primary(update: CallbackQuery | Message, state: FSMContext):
    data = await state.get_data()
    quest_number = data.get("quest_number")
    quest: Quest | None = data.get("quest")

    message: Message = update.message if isinstance(update, CallbackQuery) else update
    text = message.text if isinstance(update, Message) else update.data

    if quest.correct_answer.lower() == text.replace("answer_primary_", "").lower():
        if len(settings.MODEL_TASKS_PRIMARY) == quest_number:
            await message.answer("Вы завершили квест!")
            await state.clear()
            return

        quest.is_active = False
        await quest.save()

        kb = InlineKeyboardBuilder().button(
            text="Следующее задание",
            callback_data=f"quest_primary_{quest_number + 1}",
        )
        try:
            await message.edit_text("✅ Правильно!", reply_markup=kb.as_markup())
        except TelegramBadRequest:
            await message.answer("✅ Правильно!", reply_markup=kb.as_markup())

        await state.clear()
    else:
        await update.answer(
            "❌ Неправильно! У вас есть еще попытка...",
            show_alert=True,
            reply_markup=(
                InlineKeyboardBuilder()
                .button(text="🗑 Удалить", callback_data="del")
                .as_markup()
            ),
        )

    await update.answer() if isinstance(update, CallbackQuery) else None
