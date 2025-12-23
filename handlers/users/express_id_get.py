from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.config import EXPRESS_ID_CHANNEL, EXPRESS_ID_CHECK_CHANNEL, TEACHER_USER_ID_CHECK
from keyboards.default.buttons import start_menu, generate_regions_keyboard_button, check_your_get_id_data, \
    get_regions_keyboard, get_branches_keyboard, data
from keyboards.inline.admin_btns import check_express_id_btn, check_ref_user_id_btn
from keyboards.inline.buttons import generate_regions_keyboard, regions_data, express_id_btn1, express_id_btn2, \
    discount_button, know_address_button
from states.states import GetExpressIdState
from utils.language import LangSet
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from filters.keyboard_filter import KeyboardFilter
from utils.regex_check import check_uzbekistan_passport, is_valid_uzbekistan_phone_number, is_valid_14_digit_number, \
    is_valid_date
from utils.text_formatter import text_admin_express_id_formatter
from utils.write_to_Excel import write_to_excel_express_id
from keyboards.default.buttons import back_button

region_map = {
    'Namangan viloyati': 'TNA',
    'Fargona viloyati': 'TFA',
    'Andijon viloyati': 'TAN',
    'Sirdaryo viloyati': 'TGS',
    'Jizzax viloyati': 'TJZ',
    'Samarqand viloyati': 'TSM',
    'Navoiy viloyati': 'TYN',
    'Buxoro viloyati': 'TBO',
    'Xorazm viloyati': 'TXO',
    'Qashqadaryo viloyati': 'TQQ',
    'Surxondaryo viloyati': 'TTZ',
    'Qoraqalpogiston Respublikasi': 'TUS',
    'Toshkent viloyati': 'TOP',
    'Toshkent shahri': 'TOP',
}


@dp.message_handler(KeyboardFilter('btn_main_3'), state=None)
async def get_express_id(message: types.Message, state: FSMContext):
#     await message.answer("""
# Assalomu aleykum huramatli mijoz!
#
# Hozirda botimizda texnik xizmatlar olib borilmoqda filiallarning ochilishi munosabati bilan. Shuning uchun ID kodlar taqdim etilmayapti. Iltimos , Filiallarimiz ochilgandan keyin qayta urinib ko’ring 😇
#
# Hurmat bilan - Top Cargo !
#
# ——————————————
#
# Здравствуйте, уважаемый клиент!
#
# В настоящее время в нашем боте проводятся технические работы в связи с открытием филиалов. Поэтому на данный момент ID коды не предоставляются. Пожалуйста, попробуйте снова после открытия наших филиалов. 😇
#
# С уважением - Top Cargo!
#     """)


    data_express_check_data = await db.get_express_id_by_user_id(message.from_user.id)
    data_ref_user_id_data = await db.get_ref_users_id_by_user_id(message.from_user.id)
    if data_express_check_data and data_express_check_data['status'] == 'pending':
        text = "Sizn ID uchun so'rovingiz tekshiruvda! Iltimos kuting..."
        await message.answer(text)
        return
    elif data_express_check_data or data_ref_user_id_data:
        text = await LangSet(message.from_user.id)._('get_id_error')
        await message.answer(text, reply_markup=await know_address_button(message.from_user.id))
        return
    text = await LangSet(message.from_user.id)._('enter_name_get_id')
    await message.answer(text, reply_markup=await back_button(message.from_user.id))
    await GetExpressIdState.name.set()


@dp.callback_query_handler(text="register_user")
async def get_express_id(call: types.CallbackQuery):
    await call.answer(cache_time=3)
    data_express_check_data = await db.get_express_id_by_user_id(call.from_user.id)
    if data_express_check_data:
        text = await LangSet(call.from_user.id)._('get_id_error') + data_express_check_data['express_id']
        await call.message.answer(text, reply_markup=await start_menu(call.from_user.id))
        return
    text = await LangSet(call.from_user.id)._('enter_name_get_id')
    await call.message.answer(text, reply_markup=await back_button(call.from_user.id))
    await GetExpressIdState.name.set()


@dp.message_handler(state=GetExpressIdState.name)
async def get_express_id(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    text = await LangSet(message.from_user.id)._('enter_phone_get_id')
    #
    # back_keys = await LangSet(message.from_user.id)._('back_button1')
    # phone_key = types.KeyboardButton('☎️', request_contact=True)
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    # keyboard.row(phone_key)
    # keyboard.row(back_keys)

    await GetExpressIdState.phone_number.set()
    await message.answer(text, reply_markup=await back_button(message.from_user.id))


#
# @dp.message_handler(state=GetExpressIdState.phone_number, content_types=types.ContentType.CONTACT)
# async def get_express_id(message: types.Message, state: FSMContext):
#     phone_number = message.contact.phone_number
#
#     if message.contact.phone_number.startswith('+'):
#         phone_number = message.contact.phone_number[1:]
#     await state.update_data(phone_number=phone_number)
#     text = await LangSet(message.from_user.id)._('enter_passport_seria_get_id')
#
#     await GetExpressIdState.next()
#     await message.answer(text, reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.phone_number, content_types=types.ContentType.TEXT)
async def get_express_id(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not is_valid_uzbekistan_phone_number(phone_number):
        # back_keys = await LangSet(message.from_user.id)._('back_button1')
        # phone_key = types.KeyboardButton('☎️', request_contact=True)
        # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
        # keyboard.row(phone_key)
        # keyboard.row(back_keys)
        text = await LangSet(message.from_user.id)._('get_express_id_number_error_text')
        await message.answer(text, reply_markup=await back_button(message.from_user.id))
        return

    await state.update_data(phone_number=phone_number)
    text = await LangSet(message.from_user.id)._('enter_passport_seria_get_id')

    await GetExpressIdState.passport_seria.set()
    await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/passport_seriya.jpg'),
        caption=text,
        reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.passport_seria)
async def get_express_id(message: types.Message, state: FSMContext):
    if not check_uzbekistan_passport(message.text):
        text = await LangSet(message.from_user.id)._('passport_id_error')
        await message.answer(text)
        return
    await state.update_data(passport_seria=message.text)
    text = await LangSet(message.from_user.id)._('enter_passport_info_get_id')
    await GetExpressIdState.passport_info.set()
    # await message.answer(text, reply_markup=generate_regions_keyboard())
    await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/passport_pnfl.jpg'),
        caption=text, reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.passport_info)
async def get_express_id(message: types.Message, state: FSMContext):
    if not is_valid_14_digit_number(message.text):
        text = await LangSet(message.from_user.id)._('enter_passport_info_get_id')
        await message.answer(text, reply_markup=await back_button(message.from_user.id))
        return
    await state.update_data(passport_info=message.text)
    text = await LangSet(message.from_user.id)._('enter_birthdate_get_id')
    await GetExpressIdState.birthdate.set()
    await message.answer(text, reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.birthdate)
async def get_express_id(message: types.Message, state: FSMContext):
    if not is_valid_date(message.text):
        text = await LangSet(message.from_user.id)._('enter_birthdate_get_id')
        await message.answer(text, reply_markup=await back_button(message.from_user.id))
        return
    await state.update_data(birthdate=message.text)
    text = await LangSet(message.from_user.id)._('enter_your_address_get_id')
    await GetExpressIdState.address.set()
    await message.answer(text, reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.address)
async def get_express_id(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    text = await LangSet(message.from_user.id)._('enter_filial_get_id')
    await GetExpressIdState.filial.set()
    await message.answer(text, reply_markup=get_regions_keyboard())




# Viloyat tanlanganda
@dp.message_handler(state=GetExpressIdState.filial)
async def process_region(message: types.Message, state: FSMContext):
    region_name = message.text
    text = await LangSet(message.from_user.id)._('enter_filial_get_id')
    # Agar noto‘g‘ri viloyat tanlansa
    if region_name not in [list(item["region"].keys())[0] for item in data]:
        await message.answer(text, reply_markup=get_regions_keyboard())
        return

    await state.update_data(filial=region_name)

    # Agar viloyatda tumanlar bo‘lsa
    for item in data:
        if region_name in item["region"]:
            if "branches" in item:
                await message.answer("Iltimos, filialni tanlang:", reply_markup=get_branches_keyboard(region_name))
                await GetExpressIdState.branch.set()
                return
            # else:
            #     await message.answer('Hozircha bu viloyatdan ID CODE olish imkoniyati yo\'q.', reply_markup=await start_menu(message.from_user.id))
            #     await state.finish()
            #     return

    # Agar tumanlar bo‘lmasa, viloyat ID'sini yuboramiz
    region_code = [item["region"][region_name] for item in data if region_name in item["region"]][0]
    await state.update_data(region_code=region_code)

    text = await LangSet(message.from_user.id)._('enter_passport_front_get_id')
    await GetExpressIdState.passport_front.set()
    await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/passport_front.jpg'),
        caption=text,
        reply_markup=await back_button(message.from_user.id))

    # await message.answer(f"Tanlangan viloyat: {region_name}\nID: {region_code}", reply_markup=types.ReplyKeyboardRemove())
    # await state.finish()

# Tuman tanlanganda
@dp.message_handler(state=GetExpressIdState.branch)
async def process_branch(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    region_name = user_data.get("filial")

    if message.text == "⬅️ Orqaga":
        await message.answer("Iltimos, viloyatni tanlang:", reply_markup=get_regions_keyboard())
        await GetExpressIdState.filial.set()
        return

    for item in data:
        if region_name in item["region"] and "branches" in item:
            if message.text in item["branches"]:
                branch_code = item["branches"][message.text]
                await state.update_data(branch=message.text)
                await state.update_data(branch_code=branch_code)
                text = await LangSet(message.from_user.id)._('enter_passport_front_get_id')
                await GetExpressIdState.passport_front.set()
                await message.answer_photo(
                    photo=types.InputFile(path_or_bytesio='photos/passport_front.jpg'),
                    caption=text,
                    reply_markup=await back_button(message.from_user.id))
                return

    await message.answer("Iltimos, quyidagi tumanlardan birini tanlang.", reply_markup=get_branches_keyboard(region_name))








# @dp.message_handler(state=GetExpressIdState.filial)
# async def get_express_id(message: types.Message, state: FSMContext):
#     await state.update_data(filial=message.text)
#     text = await LangSet(message.from_user.id)._('enter_passport_front_get_id')
#     await GetExpressIdState.next()
#     await message.answer_photo(
#         photo=types.InputFile(path_or_bytesio='photos/passport_front.jpg'),
#         caption=text,
#         reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.passport_front, content_types=types.ContentType.PHOTO)
async def get_express_id(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(passport_front=photo_id)
    text = await LangSet(message.from_user.id)._('enter_passport_back_get_id')
    await GetExpressIdState.next()
    await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/passport_back.jpg'),
        caption=text,
        reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=GetExpressIdState.passport_back, content_types=types.ContentType.PHOTO)
async def get_express_id(message: types.Message, state: FSMContext):
    await state.update_data(passport_back=message.photo[-1].file_id)
    data = await state.get_data()
    text = (f"<b>Full name:</b> <i>{data['name']}</i>\n"
            f"<b>Phone number:</b> <i>{data['phone_number']}</i>\n"
            f"<b>Passport ID:</b> <i>{data['passport_seria']}</i>\n"
            f"<b>Passport info:</b> <i>{data['passport_info']}</i>\n"
            f"<b>Birthdate:</b> <i>{data['birthdate']}</i>\n"
            f"<b>Address:</b> <i>{data['address']}</i>\n"
            f"<b>Filial:</b> <i>{data['filial']}</i>\n")
    media_group = [
        types.InputMediaPhoto(media=data['passport_front']),
        types.InputMediaPhoto(media=data['passport_back'], caption=text)
    ]
    await message.answer_media_group(media_group)
    text = await LangSet(message.from_user.id)._('check_your_data_get_id')
    await message.answer(text, reply_markup=await check_your_get_id_data(message.from_user.id))
    await GetExpressIdState.next()


@dp.message_handler(KeyboardFilter('btn_check'), state=GetExpressIdState.check_data)
async def get_express_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    branch_code = data.get('branch_code')
    dto_user = await db.get_referral_user_by_user_id(message.from_user.id)

  
    if branch_code:
        filial=data.get('branch')
        id_code = data['branch_code']
    else:
        filial = data.get('filial')
        id_code = data['region_code']
    data_id = await db.get_id_by_code(id_code)
    if data_id:
        new_id_code = f"{id_code}-{str(int(data_id[0]['express_id'][4:]) + 1)}"
    else:
        new_id_code = f"{id_code}-2900"
    result = await db.select_last_added_express_id()


    try:
        data_id = await db.add_express_id(
            user_id=message.from_user.id,
            express_id=new_id_code,
            full_name=data['name'],
            phone_number=data['phone_number'],
            passport_seria=data['passport_seria'],
            passport_pnfl=data['passport_info'],
            birth_date=data['birthdate'],
            address=data['address'],
            filial=filial,
            passport_front=data['passport_front'],
            passport_back=data['passport_back']
        )
        media_group = [
            types.InputMediaPhoto(media=data['passport_front']),
            types.InputMediaPhoto(media=data['passport_back'],
                                  caption=text_admin_express_id_formatter(new_id_code, data, filial))
        ]

        data_channel = await db.get_branch_channel_by_branch_code(id_code)
        if data_channel:
            result = (await bot.send_media_group(
                chat_id=data_channel['channel_id'],
                media=media_group
            ))
            await bot.send_message(
                chat_id=data_channel['channel_id'],
                text="Ushbu malumotlar to'g'rimi?",
                reply_to_message_id=result[0].message_id,
                reply_markup=check_express_id_btn(data_id, result[0].message_id, message.from_user.id))
        else:
            result = (await bot.send_media_group(
                chat_id=EXPRESS_ID_CHECK_CHANNEL,
                media=media_group
            ))
            await bot.send_message(
                chat_id=EXPRESS_ID_CHANNEL,
                text="Ushbu malumotlar to'g'rimi?",
                reply_to_message_id=result[0].message_id,
                reply_markup=check_express_id_btn(data_id, result[0].message_id, message.from_user.id))
        text = await LangSet(message.from_user.id)._('your_request_sent_get_id')
        new_text = text.replace('#son', f"#{str(data_id)}")
        await message.answer(new_text, reply_markup=await start_menu(message.from_user.id))
        await state.finish()
    except Exception as err:
        print(err)
    return
