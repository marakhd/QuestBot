from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from tortoise.expressions import Q

from textwrap import dedent

from config import ScoringRules, settings
from db import User, Class, Quest, Score

from states import AdditionalTask, QuestState

router = Router()


# Функция для создания клавиатуры выбора класса
async def create_class_selection_kb():
    kb = InlineKeyboardBuilder()
    for class_ in await Class.filter(is_active=True).order_by('id'):  # Асинхронно получаем все классы
        kb.button(text=class_.name, callback_data=f"class_{class_.id}")
    return kb.adjust(2).as_markup()


start_text = lambda message: dedent(
    f"""Здравствуйте, {message.from_user.full_name}.

Вы попали на квест <code>Весенний Brain Rush</code>

Чтобы продолжить выберите свой класс:"""
)


# Обработчик для команды /start
@router.message(CommandStart())
async def start(message: Message):
    user = await User.get_or_none(
        tg_id=message.from_user.id,
    )

    if not user:
        await message.answer(start_text(message), reply_markup=await create_class_selection_kb())
    else:
        class_ = await Class.get_or_none(id=user.class_id) 

        if class_:
            await message.answer(
                f"Вы уже зарегистрированны в {class_.name}. Перейти к вопросу можно по кнопке.",
                reply_markup=[[InlineKeyboardButton(text="Перейти к вопросу", callback_data=f"quest_{class_.last_task}")]],
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
    class_id = int(callback.data.split("_")[1])
    class_ = await Class.get(id=class_id).prefetch_related("capitan_id")

    kb = (InlineKeyboardBuilder()
         .button(text="Выбрать другой класс", callback_data="choose_another_class")
         .button(text="Все верно", callback_data=f"continue_{class_id}"))

    capitan = class_.capitan_id

    await callback.message.edit_text(
        f"Вы выбрали класс {class_.name}\n\n"
    + (f'Капитан - <a href="tg://user?id={capitan.tg_id}">{capitan.full_name}</a> '
        f'({capitan.tg_username if capitan.tg_username else "Юзернейма нет"})\n\n' if capitan else "Капитана нет!\n")
    + f"Состояние: {"запущен" if class_.state_game else "не запущен"}", reply_markup=kb.as_markup())


# Обработчик для кнопки "Выбрать другой класс"
@router.callback_query(F.data == "choose_another_class")
async def choose_another_class(callback: CallbackQuery):
    await callback.message.edit_text(
        start_text(callback), reply_markup=await create_class_selection_kb())


@router.callback_query(F.data.startswith("continue_"))
async def start_quest(callback: CallbackQuery):
    class_id = int(callback.data.split("_")[1])
    class_ = await Class.get(id=class_id)

    user = await User.get_or_create(
        tg_id=callback.from_user.id,
        defaults={
            "tg_username": callback.from_user.username,
            "class_id": class_,
            "full_name": callback.from_user.full_name,
        },
    )

    kb = InlineKeyboardBuilder().button(
        text="Перейти к квесту", callback_data=f"quest_{class_.last_task}")

    # Если капитан не выбран, добавляем кнопку для становления капитаном
    if not class_.capitan_id:
        kb.button(text="Стать капитаном", callback_data="capitan_choice")

    await callback.answer()

    await callback.message.edit_text(f"""Вы выбрали класс {class_.name}. Начинаем квест!

Вам предстоит пройти {len(settings.model_tasks)} заданий, чтобы побороться за свой сертификат.

Также у вас будет возможность выполнить доп. задание "со звездочкой" и получить доп. {ScoringRules.VIDEO} баллов 

Приступим?""", reply_markup=kb.as_markup())


@router.callback_query(F.data == "capitan_choice")
async def capitan_choice(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "Для вашего класса пока не выбран капитан, и именно ты можешь им стать - просто нажми кнопку ниже...",
        reply_markup=[[
            InlineKeyboardButton(callback_data="capitan_selected", text="Стать капитаном")
        ]])


@router.callback_query(F.data == "capitan_selected")
async def capitan_selected(callback: CallbackQuery):
    user = await User.get(tg_id=callback.from_user.id)
    class_ = await Class.get(id=user.class_id)

    await Class.update_or_create(id=class_.id, defaults={"capitan_id": user})

    await callback.answer()
    await callback.message.edit_text("Вы стали капитаном класса!",
                                    reply_markup=InlineKeyboardBuilder().button(
                                        text="Перейти к квестам",
                                        callback_data=f"quest_{class_.last_task}"
                                    ).as_markup())


@router.callback_query(F.data.startswith("quest_"))
async def quest(callback: CallbackQuery, state: FSMContext):
    quest_number = int(callback.data.split("_")[1])
    quest_type = settings.model_tasks[quest_number - 1]
    user = await User.get(tg_id=callback.from_user.id).prefetch_related("class_id")
    class_ = user.class_id

    quests = await Quest.filter(
        (Q(for_class=class_) | Q(for_class=None)),
        type=quest_type,
        is_active=True
    ).order_by("for_class")                                                                          # Получаем все задания для класса

    if not quests:
        await callback.answer("Задания не найдены")
        return

    active_quest = None
    for quest in quests:
        if Score.get_or_none(quest=quest, class_=class_):
            active_quest = quest
            break

    if not active_quest:
        await callback.answer("Задания не найдены")
        return

    await state.set_data({"quest": active_quest, "quest_number": quest_number})

    await callback.answer()
    await callback.message.delete()
    if quest_type == "TEXT" or quest_type == "CROSSWORD":
        await callback.message.answer(f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
""")
    elif quest_type == "MUSIC":
        await callback.message.answer_audio(active_quest.data, caption=f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
""")
    elif quest_type == "PIC":
        await callback.message.answer_photo(active_quest.data, caption=f"""
Задание {quest_number} из {len(settings.model_tasks)}\n\n
{active_quest.text}\n\n
Ответ: {active_quest.answer}
""")

    await state.set_state(QuestState.answer)

    for user in await User.filter(class_id=class_.id):
        await callback.bot.send_message(
            chat_id=user.tg_id,
            text=f"Задание {quest_number} из {len(settings.model_tasks)}\n\n\n\n"
            f"Кто то уже решил задание, вы можете посмотреть следущее, нажмите на кнопку",
            reply_markup=[[InlineKeyboardButton(text="Получить задание", callback_data=f"quest_{quest_number}")]]
        )


@router.message(QuestState.answer)
async def answer_quest(message: Message, state: FSMContext):
    data = await state.get_data()
    quest: Quest = data["quest"]
    user = await User.get(tg_id=message.from_user.id)
    class_ = await Class.get(id=user.class_id)

    condition = data.get("quest_number") < len(settings.model_tasks)

    if message.text.lower() == quest.answer.lower():
        await message.answer("Правильно!")
        await Score.create(quest=quest, class_=class_, score=getattr(ScoringRules, quest.type))
        await state.clear()
        await message.answer("Перейти к следующему заданию?" if condition \
            else f"Основные задания завершены!\nВы можете перейти на задание со звездочкой (Можно получить до {ScoringRules.VIDEO} баллов) или закончить квест",
            reply_markup=[[InlineKeyboardButton(text="Да", callback_data=f"quest_{data.get("quest_number") + 1}")]] if condition else [[
                InlineKeyboardButton(text="Да", callback_data="additional_task_star"),
                InlineKeyboardButton(text="Завершить")]])
    else:
        await message.answer("Неправильно, попробуйте еще раз!")


@router.callback_query(F.data == "additional_task_star")
async def additional_task_star(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Загрузите видео поздравление девочек с 8 марта")
    await state.set_state(AdditionalTask.download_video)


@router.message(AdditionalTask.download_video, F.video)
async def download_video(message: Message, state: FSMContext):
    msg = await message.answer("Загрузка видео...")
    for admin_id in settings.ADMINS:
        await message.forward(chat_id=admin_id)
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"""Отправил видео поздравление от {message.from_user.full_name}
Класс: {await Class.get(id=User.get(tg_id=message.from_user.id).class_id).name}""")
    
    await Class.filter(id=User.get(tg_id=message.from_user.id).class_id).limit(1).update(is_active=False)
    await state.clear()
    
    msg = await msg.edit_text("Видео загружено, спасибо!")
    await message.answer("Квест завершен! Спасибо за участие, результат вы узнаете на линейке в понедельник!")


@router.callback_query(F.data == "end_quest")
async def end_quest(callback: CallbackQuery):
    await Class.filter(id=User.get(tg_id=callback.from_user.id).class_id).limit(1).update(is_active=False)

    await callback.answer()
    await callback.message.edit_text("Квест завершен! Спасибо за участие, результат вы узнаете на линейке в понедельник!")

