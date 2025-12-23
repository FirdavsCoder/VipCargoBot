import asyncio
import json

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.keyboard_filter import IsSuperAdmin, KeyboardFilter
from keyboards.default.buttons import start_menu
from keyboards.inline.admin_btns import admin_menu, branch_admin_menu
from keyboards.inline.teacher_buttons import teacher_dashboard
from loader import dp, db, bot
from utils.db_api.read_id_db import id_Excel_read
from utils.language import LangSet


def load_admins():
    with open("admins.json", "r", encoding="utf-8") as file:
        return json.load(file)["admins"]



@dp.message_handler(KeyboardFilter(keys='back_button1'), chat_type='private', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = await LangSet(message.from_user.id)._('back_text')
    await message.answer(text, reply_markup=await start_menu(message.from_user.id))




@dp.message_handler(IsSuperAdmin(), commands=['admin'], state='*')
async def admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Admin panel", reply_markup=await admin_menu(message.from_user.id))

@dp.message_handler(commands=['admin'], state='*')
async def admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    admins = await db.get_branch_data_by_admin_id(message.from_user.id)
    if admins:
        await message.answer("Admin panel", reply_markup=await branch_admin_menu())
    else:
        await message.answer("Siz admin emassiz!")


@dp.message_handler(IsSuperAdmin(), commands=['warning'])
async def warning_panel(message: types.Message):
    users = await db.get_all_users_not_payed()
    for user in users:
        user_id = user['user_id']
        caption = f"""
Muhim Eslatma ❗️
Agar sizga eski fotohisobot borgan bo’lsa , to’lov qildim tugmasini bosip shu top cargo rasmini yuvoring va boshqa malumotlaniyam ohirgacha toldiring shunda sizning yukingiz olib ketilgani tasdiqlanadi ❗️
    """
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=types.InputFile(path_or_bytesio='photos/topcargo_logo.png'),
                caption=caption
            )
            await asyncio.sleep(0.34)
        except Exception as e:
            print(e)
            pass
    await message.answer("Warning panel", reply_markup=await admin_menu(message.from_user.id))


@dp.message_handler(commands=['panel'])
async def teacher_panel(message: types.Message):
    data = await db.get_ref_link_by_user_id(message.from_user.id)
    if not data:
        await message.answer("Siz kurator emassiz!")
        return
    await message.answer(f"😊 Assalomu alaykum, {data['name']} kurator paneliga xush kelibsiz!",
                         reply_markup=teacher_dashboard)
    await message.delete()


@dp.message_handler(commands=['ref'])
async def get_ref_link(message: types.Message):
    await id_Excel_read()
