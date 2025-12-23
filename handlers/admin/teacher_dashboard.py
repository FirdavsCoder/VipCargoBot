from aiogram.dispatcher import FSMContext
from datetime import datetime
from data.config import TRANSACTION_CHECKER_ADMIN, TEACHER_PAYMENT_SUCCESS
from keyboards.default.buttons import back_button, start_menu
from keyboards.inline.teacher_buttons import teacher_dashboard, withdraw_buttons, yes_or_no_buttons, \
    settings_menu_teacher, question_payment, teacher_payment_success_btn_markup
from loader import dp, db, bot
from aiogram import types

from states.states import CardDataGetState, PaymentScreenshotState
from utils.regex_check import is_valid_card_number


@dp.callback_query_handler(text="get_ref_link")
async def get_ref_link(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.answer(f"🔗 Sizning referral ssilkangiz:\n{data['link']}", reply_markup=teacher_dashboard)
    await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="get_statistics")
async def get_statistics(call: types.CallbackQuery):
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    # await call.message.answer(f"📊 Sizning statistikangiz:\n\n🔗 Ssilkalar soni: {data['count']}\n💵 Sizga to'langan summa: {data['price']} $", reply_markup=teacher_dashboard)
    transaction_dto = await db.get_transaction_by_teacher_id(call.from_user.id)
    transaction_dto2 = await db.get_amount_by_teacher_id(call.from_user.id)
    referral_users_dto = await db.get_referral_user_by_teacher_id(call.from_user.id)
    referral_users_id = await db.get_ref_users_id_by_teacher_id(call.from_user.id)
    text = (f"✅ Muvaffaqiyatli tranzaksiyalaringiz soni: {transaction_dto[0]['count']}\n\n"
            f"💰 Tranzaksiyalaringiz summasi: {transaction_dto2}$\n\n"
            f"🔗 Siz taklif qilgan foydalanuvchilar soni: {referral_users_dto[0]['count']}\n\n"
            f"🆔 Siz taklif qilgan foydalanuvchilardan ID olganlar soni: {referral_users_id[0]['count']}\n\n")
    text += f'\n📅 {date_time}'
    await call.message.edit_text(
        text=text,
        reply_markup=teacher_dashboard
    )
    # await call.answer(text="Developing...", show_alert=True)
    # await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="get_balance")
async def get_balance(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.edit_text(f"💵 Sizning balansingiz: {data['balance']} $", reply_markup=withdraw_buttons)
    # await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="back_to_dashboard")
async def back_to_dashboard_button(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.edit_text(f"😊 Assalomu alaykum, {data['name']} kurator paneliga xush kelibsiz!",
                                 reply_markup=teacher_dashboard)


@dp.callback_query_handler(text="withdraw_my_money")
async def withdraw_my_money(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    if data['card_number'] is not None and data['card_name'] is not None:
        print(data['balance'])
        if float(data['balance']) <= float(5):
            await call.message.edit_text(
                text=f"Sizning karta malumotlaringiz:\n\n💳 {data['card_number']}\n👤 {data['card_name']}\n\n💵 Sizning balansingiz: {data['price']} $\n\n❌ <b>Siz pul yechib ololmaysiz! Pul yechish uchun balansingiz kamida 5$ yokida undan ham kop bo'lishi kerak."
                     f"Iltimos balansingiz minimal pul yechish summasiga yetishini kuting!</b>",
                reply_markup=teacher_dashboard)
            return
        await call.message.edit_text(text=f"Sizning karta malumotlaringiz:\n\n💳 {data['card_number']}\n"
                                          f"👤 {data['card_name']}\n\n💵 Sizning balansingiz: {data['price']} $\n\n"
                                          f"💰 Malumotlarni tekshirib chiqing, pullaringizni shu kartaga yechmoqchimisiz?",
                                     reply_markup=question_payment)
    elif data['card_number'] is None and data['card_name'] is None:
        await call.message.edit_text(text="Iltimos, HUMO/UZCARD kartangizni 16 ta lik raqamini kiriting: ",
                                     reply_markup=await back_button(call.from_user.id))
        await CardDataGetState.card_number.set()
    await call.answer()


@dp.message_handler(state=CardDataGetState.card_number)
async def get_card_number(message: types.Message, state: FSMContext):
    data = await db.get_ref_link_by_user_id(message.from_user.id)
    if not data:
        await message.answer("Siz kurator emassiz!")
        return
    dto = is_valid_card_number(message.text)
    if not dto:
        await message.answer("Karta raqami noto'g'ri kiritildi! Iltimos, qayta urinib ko'ring: ")
        return
    await state.update_data(card_number=message.text)
    await message.answer("Iltimos, karta egasi ismini kiriting: ")
    await CardDataGetState.card_name.set()


@dp.message_handler(state=CardDataGetState.card_name)
async def get_card_name(message: types.Message, state: FSMContext):
    await state.update_data(card_name=message.text)
    data = await state.get_data()
    await message.answer("Malumotlaringiz to'g'rimi?\n\n💳 " + data['card_number'] + "\n👤 " + data['card_name'],
                         reply_markup=yes_or_no_buttons)
    await CardDataGetState.next()


@dp.callback_query_handler(text="yes_right", state=CardDataGetState.check_data)
async def yes_right(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.update_card_data(card_number=data['card_number'], card_name=data['card_name'], user_id=call.from_user.id)
    await call.message.edit_text("Malumotlar saqlandi!", reply_markup=teacher_dashboard)
    await state.finish()
    await call.answer()


@dp.callback_query_handler(text="no_wrong")
async def no_wrong(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Iltimos, malumotlarni qayta kiritishingiz kerak yoki sozlamalardan almashtiring!",
                                 reply_markup=teacher_dashboard)
    await state.finish()
    await call.answer()


@dp.callback_query_handler(text="settings_teacher")
async def settings_teacher(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.edit_text("Kurator sozlamalari", reply_markup=settings_menu_teacher)
    await call.answer()
    # await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="edit_card_datas")
async def edit_card_datas(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.answer(text="Iltimos, HUMO/UZCARD kartangizni 16 ta lik raqamini kiriting: ",
                              reply_markup=await back_button(call.from_user.id))
    await CardDataGetState.card_number.set()
    await call.message.delete()
    await call.answer()


@dp.callback_query_handler(text="pay_request")
async def pay_request(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await db.add_transaction(
        teacher_id=call.from_user.id,
        amount=data['balance'],
        status="pending"
    )
    await bot.send_message(
        chat_id=TRANSACTION_CHECKER_ADMIN,
        text=f"Kuratorga to'lov so'rovi!\n\n"
             f"<i>Kurator:</i> <b>{data['name']}</b>\n"
             f"<i>Kurator ID:</i> <b>{data['user_id']}</b>\n"
             f"<i>Kurator bilan kelishilgan summa:</i> <b>{data['price']} $</b>\n\n"
             f"<i>O'tkazilishi kerak bo'lgan summa:</i> <b>{data['balance']} $</b>",
        reply_markup=teacher_payment_success_btn_markup(call.from_user.id)
    )
    await call.message.edit_text("So'rov yuborildi!", reply_markup=teacher_dashboard)
    await call.answer()


@dp.callback_query_handler(text="cancel_request")
async def cancel_request(call: types.CallbackQuery):
    data = await db.get_ref_link_by_user_id(call.from_user.id)
    if not data:
        await call.message.answer("Siz kurator emassiz!")
        return
    await call.message.edit_text("So'rov bekor qilindi!", reply_markup=teacher_dashboard)
    await call.answer("Bekor qilindi...", show_alert=True)
    await call.answer()


@dp.callback_query_handler(text_contains='payment_success')
async def payment_success(call: types.CallbackQuery, state: FSMContext):
    await PaymentScreenshotState.photo.set()
    teacher_id = int(call.data.split(":")[1])
    await state.update_data(teacher_id=teacher_id)
    await call.message.answer("Iltimos, to'lovni tasdiqlash uchun screenshotni yuboring: ",
                              reply_markup=await back_button(call.from_user.id))
    await call.message.delete()


@dp.message_handler(state=PaymentScreenshotState.photo, content_types=types.ContentType.PHOTO)
async def get_payment_screenshot(message: types.Message, state: FSMContext):
    data = await state.get_data()
    teacher_id = data.get("teacher_id")
    await db.update_transaction_status(teacher_id, status="success")

    data = await db.get_ref_link_by_user_id(teacher_id)
    await db.update_transaction_photo_id(teacher_id, photo_id=message.photo[-1].file_id)
    await db.update_transaction_status(teacher_id, status="success")
    # await db.update_ref_link_balance(teacher_id, balance='0')

    text = (f"✅ Kuratorga to'lov qabul qilindi!\n\n"
            f"🆔 Kurator ID: {teacher_id}\n"
            f"👤 Kurator: {data['name']}\n"
            f"💸 Kurator bilan kelishilgan summa: {data['price']} $\n"
            f"💳 To'lov summasi: {data['balance']} $")
    msg_pin_id = (
        await bot.send_photo(
            chat_id=teacher_id,
            photo=message.photo[-1].file_id,
            caption="To'lov qabul qilindi! Rahmat!"
        )

    ).message_id
    await bot.pin_chat_message(
        chat_id=teacher_id,
        message_id=msg_pin_id
    )
    await bot.send_photo(
        chat_id=TEACHER_PAYMENT_SUCCESS,
        photo=message.photo[-1].file_id,
        caption=text

    )

    await message.answer("To'lov qabul qilindi! Rahmat!", reply_markup=await start_menu(message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text_contains='payment_cancel')
async def payment_cancel(call: types.CallbackQuery):
    teacher_id = int(call.data.split(":")[1])
    await db.update_transaction_status(teacher_id, status="rejected")
    await bot.send_message(
        chat_id=teacher_id,
        text="To'lov bekor qilindi!"
    )
    await call.answer("To'lov bekor qilindi!", show_alert=True)
    await call.message.delete()
