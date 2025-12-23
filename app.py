import asyncio

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from notify_to_pay import daily_tasks
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()
    await db.create_table_users()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    # asyncio.create_task(daily_tasks())



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
