from loader import db, dp, bot
from aiogram import types
from utils.language import LangSet

from datetime import datetime

from keyboards.inline.admin_btns import admin_menu
from keyboards.inline.buttons import back_button_inline
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import mimetypes

from states.states import AchchotSentRefUserState
from utils.excel_read import read_excel_ref_user_achchot


@dp.callback_query_handler(text="complaints_sending_ref_users")
async def complaints_sending_(call: types.CallbackQuery):
    await call.message.edit_text(text="Excel faylni kiriting.", reply_markup=back_button_inline)
    await call.answer(cache_time=5)
    await AchchotSentRefUserState.file.set()


@dp.message_handler(state=AchchotSentRefUserState.file, content_types=types.ContentType.DOCUMENT)
async def complaints_sending(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    now = datetime.now()
    file_name = f"achchot_ref_user_{now.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    print('file_download ', file_name)
    await file.download(destination_file=f"./ref_user_files/{file_name}")
    print('file_download after')
    try:
        await message.answer('File keldi! Iltimos kuting... REFUSER')
        await read_excel_ref_user_achchot(file_name=file_name)
        await message.answer("Excel fayl muvaffaqiyatli qabul qilindi!", reply_markup=await admin_menu(message.from_user.id))
        await state.finish()
    except Exception as e:
        print(e)
        await message.answer(f"Xatolik yuz berdi: {e}")
        pass


@dp.message_handler(state=AchchotSentRefUserState.file, content_types=types.ContentType.TEXT)
async def complaints_sending(message: types.Message, state: FSMContext):
    await message.answer("Faqat fayl yuboring!")


