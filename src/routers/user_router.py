from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction

import random
from textwrap import dedent
# from datetime import datetime, timedelta

from tortoise.expressions import Q

from utils import Timer
from config import ScoringRules, settings
from db import User, Class, Quest, Score

from states import AdditionalTask, QuestState

router = Router()


# Функция для создания клавиатуры выбора класса
async def create_class_selection_kb():
    kb = InlineKeyboardBuilder()
    for class_ in await Class.filter(is_active=True).order_by(
        "id"
    ):  # Асинхронно получаем все классы
        kb.button(text=class_.name, callback_data=f"class_{class_.id}")
    return kb.adjust(2).as_markup()


start_text = lambda message: dedent(
    f"""Здравствуйте, {message.from_user.full_name}.

Вы попали на квест <code>Весенний Brain Rush</code>

Чтобы продолжить выберите свой класс:"""
)


async def generate_random_task(
    class_: Class, quest_type: str, event: CallbackQuery | Message
) -> Quest | None:
    quests = await Quest.filter(
        (Q(for_class__id=class_.id) | Q(for_class=None)),
        type=quest_type,
        is_active=True,
    ).order_by("for_class__name")

    if not quests:
        await event.answer("Задания не найдены")
        return

    # Присваиваем "вес" заданиям: 1 для специфичных, 0 для общих
    weighted_quests = [
        (quest, 1 if quest.for_class_id == class_.id else 0) for quest in quests
    ]
    # Перемешиваем с учётом веса (приоритетные задания перемешиваются только между собой)
    random.shuffle(weighted_quests)
    # Сортируем так, чтобы приоритетные оставались сверху
    weighted_quests.sort(key=lambda x: x[1], reverse=True)
    # Извлекаем задания после сортировки
    quests = [quest for quest, _ in weighted_quests]

    active_quest = await anext(
        (q for q in quests if not await Score.get_or_none(quest=q, class_=class_)), None
    )
    await class_.update_or_create(id=class_.id, defaults={"last_task": active_quest})

    return active_quest


# Обработчик для команды /start
@router.message(CommandStart())
async def start(message: Message):
    user = await User.get_or_none(
        tg_id=message.from_user.id,
    ).prefetch_related("sch_class")

    if not (await message.bot.get_chat(message.chat.id)).pinned_message:
        await (
            await message.answer("Если бот перестал работать - пропишите /start")
        ).pin()
        await (
            await message.answer(
                "!!! Бот будет отключен в 15:00, вы должны успеть загрузить все ответы ДО этого времени!!!\n"
            )
        ).pin()

    if not user:
        await message.answer(
            start_text(message), reply_markup=await create_class_selection_kb()
        )
    else:
        class_: Class = user.sch_class
        await class_.fetch_related("last_task")

        if not class_.last_task:
            task = await generate_random_task(
                class_, settings.model_tasks[class_.last_task_number - 1], message
            )
            if task:
                class_.last_task = task
                await class_.save()
            else:
                message.answer("Квест завершен")

        if class_:
            kb = InlineKeyboardBuilder()
            kb.button(
                text="Перейти к вопросу",
                callback_data=f"quest_{class_.last_task_number}_{class_.last_task.id}",
            )
            if not class_.capitan:
                kb.button(text="Стать капитаном", callback_data="capitan_choice")

            if class_.last_task_number == len(settings.model_tasks):
                if class_.state_game == True:
                    await message.answer(
                        f"Основные задания завершены!\n"
                        f"Вы можете перейти на задание со звездочкой (Можно получить до {int(ScoringRules.VIDEO)} баллов) "
                        f"или закончить квест\n\n"
                        f"P.S. Вы можете получить дополнительные баллы (до 10 баллов) если напишите в описание к видео стихтворение начинающееся со строк:\n"
                        f"<blockquote>Весна, моя весна...</blockquote>",
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text="Да", callback_data="additional_task_star"
                                    ),
                                    InlineKeyboardButton(
                                        text="Завершить", callback_data="end_quest"
                                    ),
                                ]
                            ]
                        ),
                    )
                return

            await message.answer(
                f"Вы уже зарегистрированны в {class_.name}. Перейти к вопросу можно по кнопке.",
                reply_markup=kb.as_markup(),
            )
        else:
            await message.answer(
                "Вы не зарегистрированы ни в одном классе. Выберите класс из списка ниже.",
                reply_markup=await create_class_selection_kb(),
            )


@router.message(Command("service"))
async def service(message: Message):
    user = await User.get(
        tg_id=message.from_user.id,
    )
    await message.answer(
        "Сервисная информация\n\n"
        f"Ваш TgID: <code>{message.from_user.id}</code>\n"
        f"{f"Ваш ID: <code>{user.id}</code>" if user else ""}",
    )


# Обработчик для выбора класса (callback)
@router.callback_query(F.data.startswith("class_"))
async def select_class(callback: CallbackQuery):
    sch_class = int(callback.data.split("_")[1])
    class_ = await Class.get(id=sch_class).prefetch_related("capitan")

    kb = (
        InlineKeyboardBuilder()
        .button(text="Выбрать другой класс", callback_data="choose_another_class")
        .button(text="Все верно", callback_data=f"continue_{sch_class}")
    )

    capitan = class_.capitan

    await callback.message.edit_text(
        f"Вы выбрали класс {class_.name}\n\n"
        + (
            f'Капитан - <a href="tg://user?id={capitan.tg_id}">{capitan.full_name}</a> '
            f'({f"@{capitan.tg_username}" if capitan.tg_username else "Юзернейма нет"})\n\n'
            if capitan
            else "Капитана нет!\n"
        )
        + f"Состояние: {"запущен" if class_.state_game else "не запущен"}",
        reply_markup=kb.as_markup(),
    )


# Обработчик для кнопки "Выбрать другой класс"
@router.callback_query(F.data == "choose_another_class")
async def choose_another_class(callback: CallbackQuery):
    await callback.message.edit_text(
        start_text(callback), reply_markup=await create_class_selection_kb()
    )


@router.callback_query(F.data.startswith("continue_"))
async def start_quest(callback: CallbackQuery):
    sch_sch_class = int(callback.data.split("_")[1])
    class_ = await Class.get(id=sch_sch_class)

    await class_.fetch_related("last_task")

    if not class_.last_task:
        task = await generate_random_task(
            class_, settings.model_tasks[class_.last_task_number - 1], callback
        )
        if task:
            class_.last_task = task
            await class_.save()
        else:
            callback.answer("Квест завершен")

    user = await User.get_or_create(
        tg_id=callback.from_user.id,
        defaults={
            "tg_username": callback.from_user.username,
            "sch_class": class_,
            "full_name": callback.from_user.full_name,
        },
    )

    kb = InlineKeyboardBuilder().button(
        text="Перейти к квесту",
        callback_data=f"quest_{class_.last_task_number}_{class_.last_task.id}",
    )

    # Если капитан не выбран, добавляем кнопку для становления капитаном
    if not class_.capitan:
        kb.button(text="Стать капитаном", callback_data="capitan_choice")

    await callback.answer()

    await callback.message.edit_text(
        f"""Вы выбрали {class_.name} класс. Начинаем квест!

Вам предстоит выполнить {len(settings.model_tasks)} основных заданий, и 2 дополнительных.

За дополнительные задания можно получить до 30 баллов.

Приступим?""",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == "capitan_choice")
async def capitan_choice(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Для вашего класса пока не выбран капитан, и именно ты можешь им стать - просто нажми кнопку ниже...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        callback_data="capitan_selected", text="Стать капитаном"
                    )
                ]
            ]
        ),
    )


@router.callback_query(F.data == "capitan_selected")
async def capitan_selected(callback: CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id).prefetch_related("sch_class")
    class_: Class = user.sch_class
    await class_.fetch_related("last_task")

    await Class.update_or_create(
        id=class_.id, defaults={"capitan": user, "state_game": True}
    )

    await callback.answer()
    await callback.message.edit_text(
        "Вы стали капитаном класса!",
        reply_markup=InlineKeyboardBuilder()
        .button(
            text="Перейти к квестам",
            callback_data=f"quest_{class_.last_task_number}_{class_.last_task.id}",
        )
        .as_markup(),
    )


@router.callback_query(F.data.startswith("quest_"))
async def quest(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    quest_number = int(data[1])
    quest_id = int(data[2]) if len(data) > 2 else None

    user = await User.get(tg_id=callback.from_user.id).prefetch_related("sch_class")
    class_: Class = user.sch_class
    quest_type = settings.model_tasks[quest_number - 1]

    # if quest_number == 1 and not class_.last_task:
    #     await Timer.start_class_timer(class_.id)

    if not class_.capitan:
        await callback.answer("Капитан не выбран", show_alert=True)
        return

    # Если quest_id не передан, выбираем случайный активный квест
    if not quest_id:
        active_quest = await generate_random_task(
            class_, settings.model_tasks[class_.last_task_number - 1], callback
        )
        if not active_quest:
            callback.answer("Квест завершен, доступных заданий не осталось")
    else:
        active_quest = await Quest.get_or_none(id=quest_id)

    if await Score.get_or_none(quest=active_quest, class_=class_):
        await callback.answer("Задание уже выполнено", show_alert=True)
        return

    if not active_quest:
        await callback.answer("Задание не найдено", show_alert=True)
        return

    await state.set_data({"quest": active_quest, "quest_number": quest_number})
    await state.set_state(QuestState.answer)

    await callback.answer()
    await callback.message.delete()

    # Отправка задания в зависимости от его типа
    if quest_type in ["TEXT", "CROSSWORD"]:
        await callback.message.answer(
            f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
"""
        )
    elif quest_type == "MUSIC":
        await callback.bot.send_chat_action(
            callback.from_user.id, ChatAction.UPLOAD_VOICE
        )
        msg = await callback.message.answer("Загрузка...")
        await msg.answer_audio(
            URLInputFile(active_quest.data),
            caption=f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
""",
        )
        await msg.delete()
    elif quest_type == "PIC":
        await callback.bot.send_chat_action(
            callback.from_user.id, ChatAction.UPLOAD_PHOTO
        )
        msg = await callback.message.answer("Загрузка...")
        await callback.message.answer_photo(
            URLInputFile(active_quest.data, timeout=60),
            caption=f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
""",
        )
        await msg.delete()


@router.message(QuestState.answer)
async def answer_quest(message: Message, state: FSMContext):
    data = await state.get_data()
    quest_number = data.get("quest_number")
    user = await User.get(tg_id=message.from_user.id).prefetch_related("sch_class")
    class_: Class = user.sch_class

    condition = quest_number < len(settings.model_tasks)

    score_count = await Score.filter(class_=class_, quest=data["quest"]).count()

    if score_count == 0:
        if message.text.lower() == data["quest"].answer.lower():
            await message.answer("Правильно!")
            await Score.create(
                quest=data["quest"],
                class_=class_,
                score=getattr(ScoringRules, data["quest"].type),
            )

            class_.last_task_number = quest_number + 1
            await class_.save()
            await state.clear()

            if condition:
                active_quest = await generate_random_task(
                    class_, settings.model_tasks[class_.last_task_number - 1], message
                )

                if not active_quest:
                    await message.answer("Следующее задание не найдено")
                    return

                await message.answer(
                    "Перейти к следующему заданию?",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Да",
                                    callback_data=f"quest_{class_.last_task_number}_{active_quest.id}",
                                )
                            ]
                        ]
                    ),
                )
            else:
                await message.answer(
                    f"Основные задания завершены!\n"
                    f"Вы можете перейти на задание со звездочкой (Можно получить до {int(ScoringRules.VIDEO)} баллов) "
                    f"или закончить квест\n\n"
                    f"P.S. Вы можете получить дополнительные баллы (до 10 баллов) если напишите в описание к видео стихтворение начинающееся со строк:\n"
                    f"<blockquote>Весна, моя весна...</blockquote>",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Да", callback_data="additional_task_star"
                                ),
                                InlineKeyboardButton(
                                    text="Завершить", callback_data="end_quest"
                                ),
                            ]
                        ]
                    ),
                )

            for user in await User.filter(sch_class=class_.id):
                if condition:
                    if user.tg_id != message.from_user.id:
                        await message.bot.send_message(
                            chat_id=user.tg_id,
                            text=f"Задание {quest_number + 1} из {len(settings.model_tasks)}\n\n"
                            f"Кто-то уже решил задание, вы можете посмотреть следующее, нажмите на кнопку ниже",
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text="Получить задание",
                                            callback_data=f"quest_{class_.last_task_number}_{active_quest.id}",
                                        )
                                    ]
                                ]
                            ),
                        )
                else:
                    if user.tg_id != message.from_user.id:
                        await message.bot.send_message(
                            chat_id=user.tg_id,
                            text=f"Основные задания завершены!\n"
                            f"Вы можете перейти на задание со звездочкой (Можно получить до {int(ScoringRules.VIDEO)} баллов) "
                            f"или закончить квест\n\n"
                            f"P.S. Вы можете получить дополнительные баллы (до 10 баллов) если напишите в описание к видео стихтворение начинающееся со строк:\n"
                            f"<blockquote>Весна, моя весна...</blockquote>",
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text="Да",
                                            callback_data="additional_task_star",
                                        ),
                                        InlineKeyboardButton(
                                            text="Завершить", callback_data="end_quest"
                                        ),
                                    ]
                                ]
                            ),
                        )
        else:
            await message.answer("Неправильно, попробуйте еще раз!")
    else:
        await message.answer("Задание уже решено")
        await state.clear()


@router.callback_query(F.data == "additional_task_star")
async def additional_task_star(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Загрузите видео поздравление девочек с 8 марта")
    await state.set_state(AdditionalTask.download_video)


@router.message(AdditionalTask.download_video, F.video)
async def download_video(message: Message, state: FSMContext):
    msg = await message.answer("Загрузка видео...")
    user: User = await User.get(tg_id=message.from_user.id).prefetch_related(
        "sch_class"
    )
    for admin_id in settings.ADMINS:
        await message.forward(chat_id=admin_id)
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"""Отправил видео поздравление от {message.from_user.full_name}
Класс: {user.sch_class.name}""",
        )

    await Class.filter(id=user.sch_class.id).limit(1).update(is_active=False)
    await state.clear()

    msg = await msg.edit_text("Видео загружено, спасибо!")
    await message.answer(
        "Квест завершен! Спасибо за участие, результат вы узнаете на линейке в понедельник!"
    )


@router.callback_query(F.data == "end_quest")
async def end_quest(callback: CallbackQuery):
    user = User.get(tg_id=callback.from_user.id).prefetch_related("sch_class")
    await Class.filter(id=user.sch_class.id).limit(1).update(is_active=False)

    await callback.answer()
    await callback.message.edit_text(
        "Квест завершен! Спасибо за участие, результат вы узнаете на линейке в понедельник!"
    )


@router.message()
async def echo(message: Message):
    await message.answer("Пропиши /start")
