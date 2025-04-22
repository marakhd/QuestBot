from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder 

from db import Class

router = Router()

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
        f"Вы выбрали класс {class_.name}\n\n"
        + f"Состояние: {"запущен" if class_.state_game else "не запущен"}",
        reply_markup=kb.as_markup(),
    )