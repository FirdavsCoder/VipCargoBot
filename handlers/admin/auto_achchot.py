from pyexpat.errors import messages

from data.config import CARD_NUMBER, CARD_OWNER, ODDIY_PRICE, DOLLAR, SERIYA_PRICE, BREND_PRICE, ODDIY_10KG_PRICE, \
    SECOND_CARD_NUMBER, SECOND_CARD_OWNER, ADMINS, SUPER_ADMINS, AVTO_PRICE
from filters.keyboard_filter import IsSuperAdmin, KeyboardFilter
from keyboards.default.buttons import back_button, start_menu
from keyboards.inline.admin_btns import type_one_achchot_send, admin_menu, type_auto_achchot_send
from keyboards.inline.buttons import uzb_receive_btn
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.states import AutoAchchotSendState
from datetime import date

from utils.language import LangSet
from utils.user_flight_check import check_user_flight_status


@dp.callback_query_handler(text='auto_achchot_send')
async def photo_get_one_achchot(call: types.CallbackQuery, state: FSMContext):

# UNCOMMENT THIS CODE WHEN YOU ARE DEPLOYING TO PRODUCTION
    # data = await db.get_branch_data_by_admin_id(call.from_user.id)
    # if not data:
    #     await call.message.answer("Siz admin emassiz!")
    #     return
    await call.message.answer("Reys nomini kiriting: ", reply_markup=await back_button(call.message.chat.id))
    await AutoAchchotSendState.flight_name.set()


# FLIGHT NAME ENTER
@dp.message_handler(state=AutoAchchotSendState.flight_name, content_types=[types.ContentType.TEXT])
async def get_flight_name_handler(message: types.Message, state: FSMContext):
    flight_name = message.text
    await state.update_data(flight_name=flight_name)
    await message.answer("Avia reys tanlandi!")
    await message.answer("Rasmni kiriting: ", reply_markup=await back_button(message.chat.id))
    await AutoAchchotSendState.photo.set()


@dp.message_handler(state=AutoAchchotSendState.photo, content_types=types.ContentType.PHOTO)
async def photo_get_one_achchot(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    await message.answer("ID KODNI kiriting: ", reply_markup=await back_button(message.chat.id))
    await AutoAchchotSendState.id_code.set()


@dp.message_handler(state=AutoAchchotSendState.photo)
async def photo_get_one_achchot(message: types.Message, state: FSMContext):
    await message.answer("Faqat rasm yuboring!")


@dp.message_handler(state=AutoAchchotSendState.id_code)
async def get_id_code_handler(message: types.Message, state: FSMContext):
    global user_data

    express_id = message.text
    user_id = message.from_user.id

    # Agar foydalanuvchi admin bo'lsa
    if user_id in ADMINS:
        user_data = await db.get_user_id_by_express_id(express_id=express_id)

    else:
        data_branch = await db.get_branch_data_by_admin_id(user_id)
        branch_code = data_branch['branch_code']

        if not express_id.startswith(branch_code):
            await message.answer(
                "ID KOD noto'g'ri! Faqat o'zingizning filial kodingizni kiritishingiz mumkin.",
                reply_markup=await back_button(message.chat.id)
            )
            return

        user_data = await db.get_user_id_by_express_id(express_id=express_id)

    # Agar user_data topilmasa
    if not user_data:
        await message.answer(
            "Bunday ID KOD mavjud emas! Qayta kiriting: ",
            reply_markup=await back_button(message.chat.id)
        )
        return

    # ID KOD saqlanadi va keyingi state o‘tadi
    await state.update_data(id_code=user_data['express_id'])
    await message.answer("Og'irlikni kiriting: ", reply_markup=await back_button(message.chat.id))
    await AutoAchchotSendState.weight.set()


@dp.message_handler(state=AutoAchchotSendState.weight)
async def get_weight_handler(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer("Tanlang: ", reply_markup=type_auto_achchot_send())
    await AutoAchchotSendState.type.set()


@dp.callback_query_handler(state=AutoAchchotSendState.type, text_contains='type_choose_one_')
async def get_type_handler(call: types.CallbackQuery, state: FSMContext):
    global data_payment_info, cards, channel_id
    if call.from_user.id not in ADMINS:
        data_admin = await db.get_branch_data_by_admin_id(call.from_user.id)
        cards = await db.get_all_cards_by_branch_code(branch_code=data_admin['branch_code'])
        channel_data = await db.get_branch_data_by_admin_id(call.from_user.id)
        channel_id = channel_data['complaint_channel_id']
    elif call.from_user.id in ADMINS or call.from_user.id in SUPER_ADMINS:
        cards = await db.get_all_cards()
        channel_id = -1003518837394
    else:
        cards = None
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
        date_today = date.today()
        product_count = '0'
        price = 0
        if data[3] == 'ODDIY':
            price = (float(kg)* ODDIY_PRICE) * DOLLAR
        elif data[3] == 'SERIYA':
            price = (float(kg) * SERIYA_PRICE) * DOLLAR
        elif data[3] == 'BREND':
            price = (float(kg) * BREND_PRICE) * DOLLAR
        elif data[3] == 'ODDIY10KG+':
            data[3] = 'ODDIY-'
            data[4] = 'SKIDKA '
            price = (float(kg) * ODDIY_10KG_PRICE) * DOLLAR
        elif data[3] == 'AVTO':
            price = (float(kg) * AVTO_PRICE) * DOLLAR
        total_sum_formatted = f"{int(price):,}".replace(',', '.')

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
                price=str(total_sum_formatted),
                date=str(date_today),
                product_count=str(product_count),
                photo_link=str(photo),
                type_product=data[3],
                flight_name=data_state['flight_name'],
            )
        except Exception as e:
            await bot.send_message(chat_id=1849953640, text=f"Databazaga qo'shishda xatolik: {e}")
            pass
        user_id = user_data[1]
        caption = f"""
👩🏻‍💻 Hurmatli Mijoz：

<b>ID Code:</b> {id_code}
<b>Vazni:</b> {kg}
<b>Narxi:</b> {total_sum_formatted}
<b>Sana:</b> {str(date_today)}

📦 Yukingiz <b>({data[3]} {data[4]})</b> Omborimizga yetib keldi.

👩🏻‍💻 Iltimos, 48 soat ichida to'lovni amalga oshiring va quyidagi tugmani bosib to'lov qilganingizni tasdiqlovchi chekni bizga yuboring. 

{text_cards}
⚠️ 3 Kun ichida to’lov qilmasangiz 4chi kundan sizga jarima qo’llaniladi , 4chi kundan boshlab yukingizni har bir saqlangan kuni uchun 20.000 summdan jarima belgilanadi.
        """
        try:
            if id_code.startswith('TPP') or id_code.startswith('TCH'):
                print(channel_id)
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=uzb_receive_btn(data_payment_info)
                )
                print(2)
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=photo,
                    caption=caption,
                    reply_markup=uzb_receive_btn(data_payment_info)
                )
                print(3)
            else:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=photo,
                    caption=caption + "\n\n<b>‼️ To’lov qilganingizdan song, filial adminiga chekingizni yuboring</b>"
                )
                await bot.send_photo(
                    chat_id=channel_id,
                    photo=photo,
                    caption=caption + "\n\n<b>‼️ To’lov qilganingizdan song, filial adminiga chekingizni yuboring</b>"
                )
            # await state.finish()
            # await call.message.answer("Muvaffaqiyatli yuborildi!", reply_markup=await admin_menu())
            await call.message.answer("Muvaffaqiyatli yuborildi! ✅✅✅")
            flight_name = data_state['flight_name']
            await state.reset_data()
            await state.update_data(flight_name=flight_name)
            try:
                flight_name = data_state.get('flight_name')
                if not flight_name:
                    await call.message.answer("Siz avia reysni tanlamadingiz!, Iltimos avia reysni nomini kiriting: ")
                    await AutoAchchotSendState.flight_name.set()
                    return
                else:
                    await call.message.answer("Avia reys tanlandi!")
            except Exception as e:
                await bot.send_message(chat_id=ADMINS[0], text=f"Avia reysni tanlashda xatolik: {e}")
                print(e)
                pass

            try:
                print(1)
                text = await check_user_flight_status(user_id)
                print(text)
                if text:
                    print(2)
                    await bot.send_message(chat_id=user_id, text=text)
            except Exception as e:
                await bot.send_message(chat_id=ADMINS[0], text=f"Xatolik: {e}")
                print(e)
                pass

            await call.message.answer("Rasmni kiriting: ", reply_markup=await back_button(call.message.chat.id))
            await AutoAchchotSendState.photo.set()
            # await call.message.delete()
            return
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=ADMINS[0], text=f"Xatolik: {e}")
            await bot.send_message(chat_id=call.from_user.id, text=f"TEXT YUBORILMADI: <b>{id_code}</b>")
            await call.message.answer("Text yuborilmadi, malumotlar bazasiga saqlandi!",
                                      reply_markup=await admin_menu(call.from_user.id))
            await call.message.delete()
            await state.finish()
            return

    except Exception as e:
        print(e)
        pass
