import asyncio
from datetime import datetime, timedelta

from aiogram import Bot

from config import settings
from db import User, Class

class Timer:
    async def start_class_timer(self, class_id: int):
        now = datetime.now()
        class_ = await Class.get_or_none(id=class_id)

        if class_ and not class_.start_time:
            # Записываем время старта в таблицу `Class`
            await Class.filter(id=class_id).update(start_time=now)
            end_time = now + timedelta(minutes=20)

            # Запускаем фоновую задачу для отслеживания таймера
            asyncio.create_task(self.timer_notifications(class_id, end_time))

    async def timer_notifications(self, class_id: int, end_time: datetime):
        time_intervals = [15, 10, 5, 3, 2, 1, 0.5, 0.166, 0.05]  # В минутах
        bot = Bot(token=settings.BOT_TOKEN)

        for minutes in time_intervals:
            remaining_seconds = (end_time - datetime.now()).total_seconds() - minutes * 60
            if remaining_seconds > 0:
                await asyncio.sleep(remaining_seconds)

            # Проверяем, не сброшен ли таймер
            class_ = await Class.get_or_none(id=class_id)
            if not class_ or not class_.start_time:
                break  

            # Получаем список участников класса
            users = await User.filter(class_id=class_id).values_list("tg_id", flat=True)

            if minutes > 0:
                text = f"⏳ Осталось {minutes} минут!" if minutes >= 1 else f"⏳ Осталось {int(minutes * 60)} секунд!"
            else:
                text = "⏳ Время квеста истекло! К сожалению, вы не успели завершить его."

                # Сбрасываем таймер в БД
                await Class.filter(id=class_id).update(start_time=None)

            # Отправляем уведомления
            for user_id in users:
                try:
                    await bot.send_message(user_id, text)
                except Exception:
                    pass
