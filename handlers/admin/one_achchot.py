from data.config import CARD_NUMBER, CARD_OWNER, SECOND_CARD_NUMBER, SECOND_CARD_OWNER
from filters.keyboard_filter import IsSuperAdmin, KeyboardFilter
from keyboards.default.buttons import back_button, start_menu
from keyboards.inline.admin_btns import type_one_achchot_send, admin_menu
from keyboards.inline.buttons import uzb_receive_btn
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.states import OneAchchotSendState
from datetime import date

from utils.language import LangSet


@dp.message_handler(KeyboardFilter(keys='back_button1'), chat_type='private', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = await LangSet(message.from_user.id)._('back_text')
    await message.answer(text, reply_markup=await start_menu(message.from_user.id))


@dp.callback_query_handler(IsSuperAdmin(), text='one_achchot_send')
async def photo_get_one_achchot(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Rasmni kiriting: ", reply_markup=await back_button(call.message.chat.id))
    await OneAchchotSendState.photo.set()


@dp.message_handler(state=OneAchchotSendState.photo, content_types=types.ContentType.PHOTO)
async def photo_get_one_achchot(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("ID KODNI kiriting: ", reply_markup=await back_button(message.chat.id))
    await OneAchchotSendState.next()


@dp.message_handler(state=OneAchchotSendState.photo)
async def photo_get_one_achchot(message: types.Message, state: FSMContext):
    await message.answer("Faqat rasm yuboring!")


@dp.message_handler(state=OneAchchotSendState.id_code)
async def get_id_code_handler(message: types.Message, state: FSMContext):
    user_data = await db.get_user_id_by_express_id(express_id=message.text)
    if not user_data:
        await message.answer("Bunday ID KOD mavjud emas! Qayta kiriting: ",
                             reply_markup=await back_button(message.chat.id))
        return
    # await bot.send_message(
    #     chat_id=1849953640,
    #     text=f"{user_data['user_id']}"
    # )
    await state.update_data(id_code=message.text)
    await message.answer("Ogirlikni kiriting: ", reply_markup=await back_button(message.chat.id))
    await OneAchchotSendState.next()


@dp.message_handler(state=OneAchchotSendState.weight)
async def get_weight_handler(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer("Narxni kiriting: ", reply_markup=await back_button(message.chat.id))
    await OneAchchotSendState.next()


@dp.message_handler(state=OneAchchotSendState.price)
async def get_price_handler(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Tanlang: ", reply_markup=type_one_achchot_send())
    await OneAchchotSendState.next()


@dp.callback_query_handler(state=OneAchchotSendState.type, text_contains='type_choose_one_')
async def get_type_handler(call: types.CallbackQuery, state: FSMContext):
    global data_payment_info
    cards = await db.get_all_cards()
    if not cards:
        await call.message.answer("Kartalar topilmadi! Iltimos, kartani qo'shing: ", reply_markup=await admin_menu(call.from_user.id))
        return
    text_cards = ""
    for card in cards:
        text_cards += f"💳 <code>{card['card_number']}</code>\n👤 <b>{card['card_name']}</b>\n\n"
    data = call.data.split('_')
    data_state = await state.get_data()
    try:
        id_code = data_state['id_code']
        kg = data_state['weight']
        photo = data_state['photo']
        price = data_state['price']
        date_today = date.today()
        product_count = '0'

        user_data = await db.get_user_id_by_express_id_equal(express_id=str(id_code))
        if not user_data:
            user_data = await db.get_user_id_by_express_id(express_id=str(id_code))
        # await bot.send_message(
        #     chat_id=1849953640,
        #     text=f"{user_data['user_id']}"
        # )
        try:

            data_payment_info = await db.add_uzb_delivered_payment(
                user_id=int(user_data[1]),
                id_code=str(id_code),
                kg=str(kg),
                price=str(price),
                date=str(date_today),
                product_count=str(product_count),
                photo_link=str(photo),
                type_product=data[3]
            )
        except Exception as e:
            await bot.send_message(chat_id=1849953640, text=f"Databazaga qo'shishda xatolik: {e}")
            pass
        user_id = user_data[1]
        caption = f"""
👩🏻‍💻 Hurmatli Mijoz：

<b>ID Code:</b> {id_code}
<b>Vazni:</b> {kg}
<b>Narxi:</b> {price}
<b>Sana:</b> {str(date_today)}

📦 Yukingiz <b>({data[3]} {data[4]})</b> Omborimizga yetib keldi.

👩🏻‍💻 Iltimos, 48 soat ichida to'lovni amalga oshiring va quyidagi tugmani bosib to'lov qilganingizni tasdiqlovchi chekni bizga yuboring. 

{text_cards}
⚠️ 3 Kun ichida to’lov qilmasangiz 4chi kundan sizga jarima qo’llaniladi , 4chi kundan boshlab yukingizni har bir saqlangan kuni uchun 20.000 summdan jarima belgilanadi.
        """
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo,
                caption=caption,
                reply_markup=uzb_receive_btn(data_payment_info)
            )
            await state.finish()
            await call.message.answer("Muvaffaqiyatli yuborildi!", reply_markup=await admin_menu(call.from_user.id))
            await call.message.delete()
            return
        except Exception as e:
            await bot.send_message(chat_id=686987202, text=f"TEXT YUBORILMADI: <b>{id_code}</b>")
            await call.message.answer("Text yuborilmadi, malumotlar bazasiga saqlandi!",
                                      reply_markup=await admin_menu(call.from_user.id))
            await call.message.delete()
            await state.finish()
            return

    except Exception as e:
        print(e)
        pass
