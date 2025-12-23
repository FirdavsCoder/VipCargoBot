from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.keyboard_filter import IsSuperAdmin
from keyboards.default.buttons import back_button
from keyboards.inline.admin_btns import admin_menu
from loader import dp, bot, db
from states.states import TrackCodeExcelState
from utils.excel_read import read_excel_track_codes


@dp.callback_query_handler(IsSuperAdmin(), text='track_code_excel')
async def track_code_excel(cal: types.CallbackQuery):
    await cal.message.answer("Excel faylini yuboring. Iltimos to'g'ri fayl yuklayoganingizni tekshiring.")
    await TrackCodeExcelState.file.set()

@dp.message_handler(IsSuperAdmin(), state=TrackCodeExcelState.file, content_types=types.ContentType.DOCUMENT)
async def track_code_excel_file(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    now = datetime.now()
    file_name = f"./excel_files/track_code_{now.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    # file_path = f"./excel_files/track_code_{file.file_path}"
    await file.download(destination=file_name)
    await message.answer("Excel fayl yuklandi.")
    await state.update_data(file_name=file_name)
    await state.update_data(file_id=file_id)
    await message.answer('Reys nomini kiriting: ', reply_markup=await back_button(message.chat.id))
    await TrackCodeExcelState.reys.set()

@dp.message_handler(IsSuperAdmin(), state=TrackCodeExcelState.reys)
async def track_code_excel_reys(message: types.Message, state: FSMContext):
    reys = message.text
    await state.update_data(reys=reys)
    await message.answer("Reys nomi qabul qilindi.")
    data = await state.get_data()
    file_name = data.get('file_name')
    file_id = data.get('file_id')
    msg_id = (await message.reply("Excel fayl yuklanmoqda... Iltimos kuting.")).message_id
    await read_excel_track_codes(file_name=file_name, reys_name=reys)
    await bot.send_message(chat_id=message.chat.id, text="Excel fayl yuklandi.", reply_to_message_id=msg_id)
    await message.answer("Excel fayl yuklandi.", reply_markup=await admin_menu(message.from_user.id))
    await state.finish()



