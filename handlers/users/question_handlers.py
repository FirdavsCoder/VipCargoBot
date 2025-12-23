from data.config import COMPLAINT_CHANNEL_ID
from keyboards.default.buttons import start_menu, back_button
from keyboards.inline.buttons import support_btn
from loader import dp, bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from filters.keyboard_filter import KeyboardFilter
from states.states import ComplaintState
from utils.language import LangSet


@dp.message_handler(KeyboardFilter(keys='questions_btn_3'), state=None)
async def questions_btn_3_handler(message: types.Message):
    text = await LangSet(message.from_user.id)._('complaint_enter_text')
    await message.answer(text)
    await ComplaintState.complaint.set()


@dp.message_handler(state=ComplaintState.complaint)
async def complaint_name(message: types.Message, state: FSMContext):
    if len(message.text) > 200:
        text = await LangSet(message.from_user.id)._('complaint_error_length_text')
        await message.answer(text)
        return
    await state.update_data(complaint=message.text)
    text = await LangSet(message.from_user.id)._('complaint_enter_name_user')
    await message.answer(text, reply_markup=await back_button(message.from_user.id))
    await ComplaintState.next()


@dp.message_handler(state=ComplaintState.user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    text = await LangSet(message.from_user.id)._('complaint_enter_phone_number')
    await message.answer(text, reply_markup=await back_button(message.from_user.id))
    await ComplaintState.next()


@dp.message_handler(state=ComplaintState.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if len(phone_number) > 12 or len(phone_number) < 12 or not phone_number.isnumeric():
        text = await LangSet(message.from_user.id)._('get_express_id_number_error_text')
        await message.answer(text)
        return

    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    complaint = data['complaint']
    user_name = data['user_name']
    phone_number = data['phone_number']
    await state.finish()

    await bot.send_message(
        chat_id=COMPLAINT_CHANNEL_ID,
        text=f"📞 <b>Yangi ariza</b>\n\n"
             f"<b>Ariza:</b> {complaint}\n"
             f"<b>Ism:</b> {user_name}\n"
             f"<b>Telefon raqam:</b> {phone_number}\n",
        parse_mode='HTML'
    )
    text = await LangSet(message.from_user.id)._('complaint_send_Success_text')
    await message.answer(text, reply_markup=await start_menu(message.from_user.id))


# Special Questions button handler
@dp.message_handler(KeyboardFilter(keys='questions_btn_2'), state=None)
async def questions_btn_2_handler(message: types.Message):
    text = await LangSet(message.from_user.id)._('support_text')
    # await message.answer('Admin lichkasini qaytaramiz bu yerga', reply_markup=keyboard)
    await message.answer(text, reply_markup=await support_btn(message.from_user.id))
