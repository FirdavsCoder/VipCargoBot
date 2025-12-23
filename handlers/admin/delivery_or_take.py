from data.config import DELIVERED_PRODUCTS_CHANNEL, UZB_DELIVERED_PAYMENT_CHANNEL, SUCCESS_TRANSACTION_RECEIVED, \
    YANDEX_CHANNEL, TAKE_AWAY_ME_CHANNEL, EMU_CHANNEL, BTS_CHANNEL, OLD_PRODUCT_CHANNEL, NEW_PRODUCT_CHANNEL
from keyboards.default.buttons import start_menu
from keyboards.inline.buttons import delivered_success_btn, take_away_success_btn, \
    admin_delivered_btn, admin_delivered_btn_2, yes_or_new_enter_button_for_delivery_products_data, \
    choose_mail_type_buttons, choose_mail_type_tch_buttons
from loader import db, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.states import DeliveryProductState
from keyboards.default.buttons import back_button


@dp.callback_query_handler(text_contains='delivery_product')
async def delivery_product(call: types.CallbackQuery, state: FSMContext):
    id_data = call.data.split(':')[1]
    data = await db.get_data_by_id_uzb_delivered_products_payment(id=int(id_data))
    if data['status']:
        await call.answer('Siz to\'lov qilgansiz!', show_alert=True)
        await call.message.edit_reply_markup(reply_markup=delivered_success_btn)
        return
    await DeliveryProductState.photo.set()
    print(data['id'])
    await state.update_data(uzb_delivered_payment_id=data['id'])
    await call.message.answer('To\'lov chek screenshotni kiriting: ', reply_markup=await back_button(call.from_user.id))
    await state.update_data(message_id=call.message.message_id)


@dp.message_handler(state=DeliveryProductState.photo, content_types=types.ContentType.PHOTO)
async def photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    data = await db.check_delivery_data_product_by_user_id(message.from_user.id)
    await DeliveryProductState.next()
    if data:
        text = f"Oxirgi marta foydalanilgan ism: {data[2]}"
        await message.answer(text, reply_markup=await yes_or_new_enter_button_for_delivery_products_data())
    else:
        await message.answer('Ismingizni kiriting: ', reply_markup=await back_button(message.from_user.id))


@dp.callback_query_handler(text_contains='callback_delivery_', state=DeliveryProductState.name)
async def callback_delivery_handler(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[2] == 'yes':
        data = await db.check_delivery_data_product_by_user_id(call.from_user.id)
        await state.update_data(name=data[2])
        text = f"Oxirgi marta foydalanilgan telefon raqam: {data[3]}"
        await call.message.answer(text, reply_markup=await yes_or_new_enter_button_for_delivery_products_data())
        await call.message.delete()
        await DeliveryProductState.phone_number.set()
    elif data[2] == 'new':
        await DeliveryProductState.name.set()
        await call.message.answer('Ismingizni kiriting: ', reply_markup=await back_button(call.from_user.id))
        await call.message.delete()


@dp.message_handler(state=DeliveryProductState.name)
async def name(message: types.Message, state: FSMContext):
    try:
        await db.update_name_delivery_data_product_by_user_id(
            user_id=message.from_user.id,
            name=message.text
        )
    except Exception as err:
        # await message.answer(err)
        print(err)
        pass
    await state.update_data(name=message.text)
    data = await db.check_delivery_data_product_by_user_id(message.from_user.id)
    if data:
        await state.update_data(name=message.text)
        text = f"Oxirgi marta foydalanilgan telefon raqam: {data[3]}"
        await message.answer(text, reply_markup=await yes_or_new_enter_button_for_delivery_products_data())
        await DeliveryProductState.phone_number.set()
    else:
        await DeliveryProductState.next()
        await message.answer('Telefon raqamingizni kiriting: ', reply_markup=await back_button(message.from_user.id))


@dp.callback_query_handler(text_contains='callback_delivery_', state=DeliveryProductState.phone_number)
async def callback_delivery_handler(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split('_')
    if data[2] == 'yes':
        data = await db.check_delivery_data_product_by_user_id(call.from_user.id)
        await state.update_data(phone_number=data[3])
        await DeliveryProductState.next()
        await call.message.answer('Manzilni kiriting: ', reply_markup=await back_button(call.from_user.id))
        await call.message.delete()
    elif data[2] == 'new':
        await DeliveryProductState.phone_number.set()
        await call.message.answer('Telefon raqamingizni kiriting: ', reply_markup=await back_button(call.from_user.id))
        await call.message.delete()


@dp.message_handler(state=DeliveryProductState.phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    try:
        await db.update_phone_number_delivery_data_product_by_user_id(
            user_id=message.from_user.id,
            phone_number=message.text
        )
    except Exception as err:
        # await message.answer(err)
        print(err)
        pass
    # data = await db.check_delivery_data_product_by_user_id(message.from_user.id)
    # if data:
    #     text = f"Oxirgi marta foydalanilgan manzil: {data[5]}"
    #     await message.answer(text, reply_markup=await yes_or_new_enter_button_for_delivery_products_data())
    #     await DeliveryProductState.address.set()
    # else:
    await DeliveryProductState.next()
    await message.answer('Manzilni kiriting: ', reply_markup=await back_button(message.from_user.id))


# @dp.callback_query_handler(text_contains='callback_delivery_', state=DeliveryProductState.address)
# async def callback_delivery_handler(call: types.CallbackQuery, state: FSMContext):
#     data = call.data.split('_')
#     data_state = await state.get_data()
#     print(data)
#     if data[2] == 'yes':
#         print(data_state)
#         data_id = await db.get_express_id_by_user_id(user_id=call.from_user.id)
#         print(data_id)
#         print(data_state)
#         if not data_id:
#             await call.message.answer('Siz hali express ID olmagansiz! ',
#                                       reply_markup=await start_menu(call.from_user.id))
#             await state.finish()
#             return
#         try:
#             await bot.edit_message_reply_markup(
#                 chat_id=call.from_user.id,
#                 message_id=data_state['message_id'],
#                 reply_markup=delivered_success_btn
#             )
#         except Exception as err:
#             pass
#         try:
#             dto = await db.check_delivery_data_product_by_user_id(call.from_user.id)
#             info = await db.get_uzb_delivered_payment_data_by_id(id=int(data_state['uzb_delivered_payment_id']))
#             text = "Yangi dostavka 🎉"
#             text += f"\n<b>ID:</b> <code>{data_id['express_id']}</code>"
#             text += "\n\n<b>Ism:</b> " + data_state['name']
#             text += "\n<b>Telefon raqam:</b> " + data_state['phone_number']
#             text += "\n<b>Manzil:</b> " + dto[5]
#             text += (f"\n\nMahsulot malumotlari:\n"
#                      f"📦 <b>Og'irlik:</b> {info[3]}\n"
#                      f"📅 <b>Sana:</b> {info[4]}\n"
#                      f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
#                      f"💰 <b>To'lov:</b> {info[6]}")
#             await bot.send_photo(
#                 chat_id=DELIVERED_PRODUCTS_CHANNEL,
#                 photo=data_state['photo'],
#                 caption=text,
#                 reply_markup=admin_delivered_btn(data_state['uzb_delivered_payment_id'])
#             )
#             try:
#                 await db.update_uzb_delivered_payment_pic_id(id=int(data_state['uzb_delivered_payment_id']),
#                                                              pic_id=data_state['photo'])
#             except Exception as err:
#                 await bot.send_message(
#                     chat_id=1849953640,
#                     text=f"ERROR update_uzb_delivered_payment_pic_id: {err}"
#                 )
#                 print(err)
#                 pass
#         except Exception as err:
#             print(err)
#             pass
#         await call.message.answer('Muvaffaqiyatli saqlandi! ✅', reply_markup=await start_menu(call.from_user.id))
#         await call.message.delete()
#         await state.finish()
#     elif data[2] == 'new':
#         # await DeliveryProductState.address.set()
#         await call.message.delete()
#         await call.message.answer('Manzilni kiriting: ', reply_markup=await back_button(call.from_user.id))
#

@dp.message_handler(state=DeliveryProductState.address)
async def address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(address=message.text)
    # Express ID CHECK
    data_id = await db.get_express_id_by_user_id(user_id=message.from_user.id)
    if not data_id:
        await message.answer('Siz hali express ID olmagansiz! ', reply_markup=await start_menu(message.from_user.id))
        await state.finish()
        return
    await db.update_address_delivery_data_product_by_user_id(
        user_id=message.from_user.id,
        address=message.text
    )
    if not data_id['express_id'].startswith('TCH'):
        await message.answer("Yukingizni qay holda qabul qilib olishni xohlaysiz? Tanlang: ",
                             reply_markup=await choose_mail_type_buttons())
    else:
        await message.answer("Yukingizni qay holda qabul qilib olishni xohlaysiz? Tanlang: ",
                             reply_markup=await choose_mail_type_tch_buttons())
    await DeliveryProductState.next()


@dp.callback_query_handler(state=DeliveryProductState.mail_type)
async def choose_mail_type(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # Express ID CHECK
    data_id = await db.get_express_id_by_user_id(user_id=call.from_user.id)
    if not data_id:
        await call.message.answer('Siz hali express ID olmagansiz! ',
                                  reply_markup=await start_menu(call.from_user.id))
        await state.finish()
        return
    await state.finish()

    dto = await db.check_delivery_data_product_by_user_id(call.from_user.id)
    if not dto:
        await db.insert_delivery_products(
            user_id=call.from_user.id,
            name=data['name'],
            phone_number=data['phone_number'],
            uzb_id=data_id['express_id'],
            address=data['address']
        )
    try:
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=data['message_id'],
            reply_markup=delivered_success_btn
        )
    except Exception as err:
        pass
    try:
        info = await db.get_uzb_delivered_payment_data_by_id(id=int(data['uzb_delivered_payment_id']))
        text = "Yangi dostavka 🎉"
        text += f"\n<b>ID:</b> <code>{data_id['express_id']}</code>"
        text += "\n\n<b>Ism:</b> " + data['name']
        text += "\n<b>Telefon raqam:</b> " + data['phone_number']
        text += "\n<b>Manzil:</b> " + data['address']
        text += (f"\n\nMahsulot malumotlari:\n"
                 f"📦 <b>Og'irlik:</b> {info[3]}\n"
                 f"📅 <b>Sana:</b> {info[4]}\n"
                 f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
                 f"💰 <b>To'lov:</b> {info[6]}")
        if call.data == 'yandex':
            if data_id['express_id'].startswith('TCH'):
                data_data = await db.get_branch_channel_by_branch_code(data_id['express_id'][:3])
                text += "\n\n🚚 <b>Pochta turi: </b> <u><i>YANDEX</i></u>"
                await bot.send_photo(
                    chat_id=data_data['delivery_channel_id'],
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )
            else:
                text += "\n\n🚚 <b>Pochta turi: </b> <u><i>YANDEX</i></u>"
                await bot.send_photo(
                    chat_id=YANDEX_CHANNEL,
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )

        elif call.data == 'ozim_olib_ketaman':
            text += "\n\n🚚 <b>Pochta turi: </b> <u><i>O'ZI OLIB KETADI</i></u>"
            if data_id['express_id'].startswith('TCH'):
                data_data = await db.get_branch_channel_by_branch_code(data_id['express_id'][:3])
                await bot.send_photo(
                    chat_id=data_data['pickup_channel'],
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )
            else:
                await bot.send_photo(
                    chat_id=TAKE_AWAY_ME_CHANNEL,
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )
        elif call.data == 'emu':
            if data_id['express_id'].startswith('TCH'):
                data_data = await db.get_branch_channel_by_branch_code(data_id['express_id'][:3])
                text += "\n\n🚚 <b>Pochta turi: </b> <u><i>EMU</i></u>"
                await bot.send_photo(
                    chat_id=data_data['emu_channel'],
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )
            else:
                text += "\n\n🚚 <b>Pochta turi: </b> <u><i>EMU</i></u>"
                await bot.send_photo(
                    chat_id=EMU_CHANNEL,
                    photo=data['photo'],
                    caption=text,
                    reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
                )



        elif call.data == 'bts':
            text += "\n\n 🚚 <b>Pochta turi: </b> <u><i>BTS</i></u>"
            await bot.send_photo(
                chat_id=BTS_CHANNEL,
                photo=data['photo'],
                caption=text,
                reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
            )
        elif call.data == "eski_reysdagi_yuklarim_bilan_olaman":
            text += "\n\n🚚 <b>Pochta turi: </b> <u><i>ESKI REYSDAGI YUKLARIM BILAN BIRGA OLAMAN</i></u>"
            await bot.send_photo(
                chat_id=OLD_PRODUCT_CHANNEL,
                photo=data['photo'],
                caption=text,
                reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
            )
        elif call.data == "keyingi_reysdagi_yuklarim_bilan_olaman":
            text += "\n\n🚚 <b>Pochta turi: </b> <u><i>KEYINGI REYSDAGI YUKLARIM BILAN BIRGA OLAMAN</i></u>"
            await bot.send_photo(
                chat_id=NEW_PRODUCT_CHANNEL,
                photo=data['photo'],
                caption=text,
                reply_markup=admin_delivered_btn(data['uzb_delivered_payment_id'])
            )
        try:
            await db.update_uzb_delivered_payment_pic_id(id=int(data['uzb_delivered_payment_id']), pic_id=data['photo'])
        except Exception as err:
            await bot.send_message(
                chat_id=1849953640,
                text=f"ERROR update_uzb_delivered_payment_pic_id: {err}"
            )
            print(err)
            pass
    except Exception as err:
        print(err)
        pass
    await call.message.answer('Muvaffaqiyatli saqlandi! ✅', reply_markup=await start_menu(call.from_user.id))
    await call.message.delete()


@dp.message_handler(state=DeliveryProductState.mail_type)
async def choose_mail_type(message: types.Message, state: FSMContext):
    await message.answer('❌ Siz faqat tugmalardan birini tanlashingiz shart!')


@dp.callback_query_handler(text='take_away')
async def take_away(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=take_away_success_btn)


@dp.callback_query_handler(text="success_take_away")
async def success_take_away(call: types.CallbackQuery):
    await call.answer(text="Siz tovarni olib kelgan bo'lishingiz kerak. ✅", show_alert=True)


@dp.callback_query_handler(text_contains="successfully_takeout_box")
async def successfully_takeout_box(call: types.CallbackQuery):
    data = call.data.split(':')[1]
    info = await db.get_uzb_delivered_payment_data_by_id(id=int(data))
    try:
        text = (f"Sizning tovaringiz yuborildi! ✅\n\n"
                f"Mahsulot malumotlari:\n"
                f"🆔 <b>ID-CODE: {info[2]}</b>\n"
                f"📦 <b>Og'irlik:</b> {info[3]}\n"
                f"📅 <b>Sana:</b> {info[4]}\n"
                f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
                f"💰 <b>To'lov:</b> {info[6]}")
        await bot.send_photo(chat_id=info[1],
                             photo=str(info[9]),
                             caption=text)
        data_user = await db.check_delivery_data_product_by_user_id(info[1])
        cap = (f"Ushbu tovar chiqarib yuborildi! ✅\n\n"
               f"Foydalanuvchi malumotlari: \n"
               f"📄 <b>Ismi: </b> {data_user[2]}\n"
               f"📞 <b>Telefon raqami: </b> {data_user[3]}\n"
               f"🏠 <b>Manzili: </b> {data_user[5]}\n\n"
               f"Mahsulot malumotlari:\n"
               f"🆔 <b>ID-CODE: </b> {info[2]}\n"
               f"📦 <b>Og'irlik:</b> {info[3]}\n"
               f"📅 <b>Sana:</b> {info[4]}\n"
               f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
               f"💰 <b>To'lov:</b> {info[6]}")
        try:
            if info[2].startswith('TCH'):
                data_tch = await db.get_branch_channel_by_branch_code(info[2][:3])
                await bot.send_photo(
                    chat_id=data_tch['delivered_channel'],
                    photo=info[7],
                    caption=cap
                )
            else:
                await bot.send_photo(
                    chat_id=UZB_DELIVERED_PAYMENT_CHANNEL,
                    photo=info[9],
                    caption=cap,
                )
        except Exception as err:
            await call.message.answer(err)
            print(err)
            pass
    except Exception as err:
        await call.message.answer(err)
        print(err)
        pass
    await call.answer(text="Siz tovarni olib chiqarib yuborgan bo'lishingiz kerak. ✅", show_alert=True)
    await call.message.delete()


@dp.callback_query_handler(text_contains="canceled_takeout_box")
async def canceled_takeout_box(call: types.CallbackQuery):
    data = call.data.split(':')[1]
    info = await db.get_uzb_delivered_payment_data_by_id(id=int(data))
    try:
        text = (f"Sizning tovaringizni yuborish bekor qilindi! ❌\n\n"
                f"Mahsulot malumotlari:\n"
                f"🆔 <b>ID-CODE: </b>{info[2]}\n"
                f"📦 <b>Og'irlik:</b> {info[3]}\n"
                f"📅 <b>Sana:</b> {info[4]}\n"
                f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
                f"💰 <b>To'lov:</b> {info[6]}")
        await bot.send_message(chat_id=info[1],
                               text=text)
    except Exception as err:
        await call.message.answer(err)
        print(err)
        pass
    await call.answer(text="Siz tovarni olib chiqarib yubormagan bo'lishingiz kerak. ❌", show_alert=True)
    await call.message.delete()


@dp.callback_query_handler(text_contains="successfully_payment_delivered_box")
async def canceled_takeout_box(call: types.CallbackQuery):
    data = call.data.split(':')[1]
    info = await db.get_uzb_delivered_payment_data_by_id(id=int(data))
    try:
        await db.update_uzb_delivered_payment_status(id=int(data))
    except Exception as err:
        await call.message.answer(err)
        print(err)
        pass
    try:
        text = (f"Sizning to'lovingiz qabul qilindi! ✅\n\n"
                f"Mahsulot malumotlari:\n"
                f"🆔 <b>ID-CODE: </b>{info[2]}\n"
                f"📦 <b>Og'irlik:</b> {info[3]}\n"
                f"📅 <b>Sana:</b> {info[4]}\n"
                f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
                f"💰 <b>To'lov:</b> {info[6]}")
        await bot.send_message(chat_id=info[1],
                               text=text)
        data_user = await db.check_delivery_data_product_by_user_id(info[1])
        cap = (f"To'lov qabul qilindi! ✅\n\n"
               f"Foydalanuvchi malumotlari: \n"
               f"📄 <b>Ismi: </b> {data_user[2]}\n"
               f"📞 <b>Telefon raqami: </b> {data_user[3]}\n"
               f"🏠 <b>Manzili: </b> {data_user[5]}\n\n"
               f"Mahsulot malumotlari:\n"
               f"🆔 <b>ID-CODE: </b>{info[2]}\n"
               f"📦 <b>Og'irlik:</b> {info[3]}\n"
               f"📅 <b>Sana:</b> {info[4]}\n"
               f"🔢 <b>Mahsulot soni:</b> {info[5]}\n"
               f"💰 <b>To'lov:</b> {info[6]}")
        if info[2].startswith('TCH'):
            data_tch = await db.get_branch_channel_by_branch_code(info[2][:3])
            await bot.send_photo(
                chat_id=data_tch['payment_channel'],
                photo=info[7],
                caption=cap
            )
        else:
            await bot.send_photo(
                chat_id=SUCCESS_TRANSACTION_RECEIVED,
                photo=info[7],
                caption=cap
            )
    except Exception as err:
        await call.message.answer(err)
        print(err)
        pass
    await call.answer(text="Siz to'lovni qabul qilib olgan bo'lishingiz kerak ✅", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=admin_delivered_btn_2(data))
