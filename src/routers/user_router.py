from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from textwrap import dedent

from config import settings
from db import User, Class

from states import AdditionalTask, Quest

router = Router()


# Функция для создания клавиатуры выбора класса
async def create_class_selection_kb():
    kb = InlineKeyboardBuilder()
    for class_ in await Class.all():  # Асинхронно получаем все классы
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
    user = await User.get(
        tg_id=message.from_user.id,
    )

    if not user:
        kb = await create_class_selection_kb()  # Создаем клавиатуру

        await message.answer(start_text(message), reply_markup=kb)
    else:
        await message.answer("Вы уже зарегистрированы!")


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
    class_ = await Class.get(id=class_id)

    kb = InlineKeyboardBuilder()
    kb.button(text="Выбрать другой класс", callback_data="choose_another_class")
    kb.button(text="Все верно", callback_data=f"continue_{class_id}")

    capitan = User.get_or_none(class_.capitan_id)

    await callback.message.edit_text(
        f"Вы выбрали класс {class_.name}\n\n"
        f"{f"Капитан -  ({capitan.tg_username if capitan.tg_username else "Юзернейма нет"})" if capitan else ""}\n\n"
        f"Состояние: {"Не начат"}", reply_markup=kb.as_markup()
    )


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

    await callback.answer()

    await callback.message.edit_text(f"""Вы выбрали класс {class_.name}. Начинаем квест!

Вам предстоит пройти {len(settings.model_tasks)} заданий, чтобы побороться за свой сертификат.

Также у вас будет возможность выполнить доп. задание "со звездочкой" и получить доп. 10 баллов 

Приступим?""", reply_markup=[[InlineKeyboardButton(callback_data="quest_1", text="Да!")]])


@router.callback_query(F.data.startswith("quest_"))
async def quest(callback: CallbackQuery):
    quest_number = int(callback.data.split("_")[1])
    await callback.answer()
    await callback.message.edit_text("P")


@router.message(Quest.answer)
async def answer_quest(message: Message, state: FSMContext):
    await message.edit_text("", reply_markup=None)


@router.callback_query(F.data == "additional_task_star")
async def additional_task_star(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("Загрузите видео поздравление девочек с 8 марта")
    await state.set_state(AdditionalTask.download_video)


@router.message(AdditionalTask.download_video, F.video)
async def download_video(message: Message, state: FSMContext):
    await message.answer("Загрузка видео...")
    for admin_id in settings.ADMINS:
        await message.forward(chat_id=admin_id)
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"""Отправил видео поздравление от {message.from_user.full_name}
Класс: {Class.get(id=User.get(tg_id=message.from_user.id).class_id).name}""")
    


@router.callback_query(F.data == "end_quest")
async def end_quest(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Квест завершен! Спасибо за участие, результат вы узнаете на линейке в понедельник!")

