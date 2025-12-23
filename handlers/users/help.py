from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

from aiogram import types

from filters.keyboard_filter import IsSuperAdmin, IsAdmin
from keyboards.inline.admin_btns import admin_menu
from loader import dp, db, bot


@dp.message_handler(IsAdmin(), commands=['admin'])
async def admin_panel(message: types.Message):
    await message.answer("Admin panel", reply_markup=await admin_menu(message.from_user.id))


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")

    await message.answer("\n".join(text))
