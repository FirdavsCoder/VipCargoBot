from datetime import datetime

from keyboards.inline.admin_btns import admin_menu
from keyboards.inline.buttons import back_button_inline
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import mimetypes

from states.states import AchchotSendState
from utils.excel_read import read_excel_achchot, read_excel_easy


@dp.callback_query_handler(text="complaints_sending")
async def complaints_sending(call: types.CallbackQuery):
    await call.message.edit_text(text="Excel faylni kiriting.", reply_markup=back_button_inline)
    await call.answer(cache_time=5)
    await AchchotSendState.file.set()


@dp.message_handler(state=AchchotSendState.file, content_types=types.ContentType.DOCUMENT)
async def complaints_sending(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    now = datetime.now()
    file_name = f"achchot_{now.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    print('file_download ', file_name)
    await file.download(destination_file=f"./excel_files/{file_name}")
    print('file_download after')
    try:
        await message.answer('File keldi! Iltimos kuting...')
        await read_excel_easy(file_name=file_name)
        await message.answer("Excel fayl muvaffaqiyatli qabul qilindi!", reply_markup=await admin_menu(message.from_user.id))
        await state.finish()
    except Exception as e:
        print(e)
        await message.answer(f"Xatolik yuz berdi: {e}")
        pass


@dp.message_handler(state=AchchotSendState.file, content_types=types.ContentType.TEXT)
async def complaints_sending(message: types.Message, state: FSMContext):
    await message.answer("Faqat fayl yuboring!")

