import asyncio
from datetime import datetime
import pandas as pd
from aiogram.dispatcher import FSMContext

from loader import db, dp, bot
from aiogram import types
from filters.keyboard_filter import IsSuperAdmin
from states.states import SendAdState


@dp.callback_query_handler(IsSuperAdmin(), text='send_ad')
async def send_ad(call: types.CallbackQuery):
    await call.message.answer(text="Postni kiriting. E'tiborli bo'ling siz kiritgan post hamma foydalanuvchilarga "
                                   "birdaniga yuboriladi.")
    await SendAdState.post.set()
    await call.message.delete()


@dp.message_handler(IsSuperAdmin(), state=SendAdState.post, content_types=types.ContentType.ANY)
async def send_ad_post(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    for user in users:
        try:
            await bot.copy_message(
                chat_id=user['user_id'],
                from_chat_id=message.chat.id,
                message_id=message.message_id)
            await asyncio.sleep(0.04)
        except Exception as e:
            print(e)
    await state.finish()
    await message.answer("Post barcha foydalanuvchilarga yuborildi.")
