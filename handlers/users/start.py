import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.keyboard_filter import KeyboardFilter
from keyboards.default.buttons import start_menu, back_button, contact_us_buttons
from keyboards.inline.buttons import keyboard_check_is_registered
from keyboards.inline.language_keyboard import language_keyboard
from loader import dp, db, bot
from data.config import ADMINS
from states.states import CheckTrackCodeState
from utils.get_file import get_file_request
from utils.language import LangSet


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    args = message.get_args()
    user = await db.select_user(user_id=message.from_user.id)
    if user:
        text = await LangSet(message.from_user.id)._('start')
        await message.answer(text, reply_markup=await start_menu(message.from_user.id))
        # if args:
        #     data = await db.get_ref_link_by_link_code(args)
        #     if data:
        #         dto = await db.get_referral_user_by_user_id(user_id=message.from_user.id)
        #         if not dto:
        #             await bot.send_message(
        #                 chat_id=data['user_id'],
        #                 text=f"🎉 Sizning taklifingiz bilan yangi foydalanuvchi ro'yxatdan o'tdi.\n"
        #                      f"👤 Ismi: {message.from_user.full_name}\n"
        #                      f"🔗 Taklif linki: {args}"
        #             )
        #             await db.add_referral_user(
        #                 user_id=message.from_user.id,
        #                 teacher_id=data['user_id'],
        #                 name=message.from_user.full_name,
        #                 express_code=data['express_code'],
        #                 link_code=args
        #             )


# Back Button Handler
@dp.message_handler(KeyboardFilter(keys='back_button1'), chat_type='private', state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = await LangSet(message.from_user.id)._('back_text')
    await message.answer(text, reply_markup=await start_menu(message.from_user.id))


# Biz haqimizda
@dp.message_handler(KeyboardFilter(keys='btn_main_1'), state=None)
async def start(message: types.Message):
    text = await LangSet(message.from_user.id)._('select_text')
    return await message.answer(text, reply_markup=await contact_us_buttons(message.from_user.id))


@dp.message_handler(KeyboardFilter(keys='btn_main_5'), state=None)
async def settings_button(message: types.Message):
    if message.chat.type == 'private':
        text = await LangSet(message.from_user.id)._('please_select_lang')
        await message.answer(text=text, reply_markup=await language_keyboard(message.from_user.id))


# TREK CODE CHECK
@dp.message_handler(KeyboardFilter(keys='btn_main_2'), state=None)
async def start(message: types.Message):
    text = await LangSet(message.from_user.id)._('enter_id')
    await CheckTrackCodeState.track_code.set()
    return await message.answer(text, reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=CheckTrackCodeState.track_code)
async def check_track_code(message: types.Message, state: FSMContext):
    track_code = message.text
    user_id = message.from_user.id
    try:
        dto = await db.get_track_code_data_by_track_code_base(track_code)
        print(dto)
        if not dto:
            text = await LangSet(user_id)._('id_not_found_error_text_2')
            await message.answer(text, reply_markup=await back_button(user_id))
            await state.finish()
            return
        text = f"""
🔍 Tovar track kodi: <b>{track_code}</b>
🇨🇳 Xitoy omborimiz qabul qilgan kun: <b>{dto['receive_date']}</b>
📦 Tovar nomi: <b>{dto['product_name']}</b>
⚖️ Og’irligi: <b>{dto['weight']}</b>
🔢 Miqdori: <b>{dto['count']}</b>
🛬 Qaysi reysda yetib kelishi: <b>{dto['reys_name']}</b>
"""
        await message.answer(text, reply_markup=await back_button(user_id))
        await state.finish()
        return

        # data = await db.get_track_code_data_by_track_code(track_code)
        # if not data:
        #     text = await LangSet(user_id)._('id_not_found_error_text_2')
        #     await message.answer(text, reply_markup=await back_button(user_id))
        #     return
        # await state.finish()
        # txt = f"{data['express_id'], data['track_code'], data['weight'], data['type'], data['receive_china'], data['receive_uz']}"
        # text = await LangSet(user_id)._('back_text')
        # await message.answer(txt, reply_markup=await start_menu(user_id))
    except asyncpg.exceptions.UniqueViolationError:
        text = await LangSet(user_id)._('id_not_found_error_text')
        await message.answer(text, reply_markup=await back_button(message.from_user.id))


#
# @dp.message_handler(KeyboardFilter(keys='btn_main_4'), state=None)
# async def start(message: types.Message):
#     text = await LangSet(message.from_user.id)._('problem_and_complaint_text')
#     return await message.answer(text, reply_markup=await start_menu(message.from_user.id))


@dp.callback_query_handler(text="know_id_address")
async def know_address_handler(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    dto = await db.get_express_id_by_user_id(call.from_user.id)
    data_ref_user_id_data = await db.get_ref_users_id_by_user_id(call.from_user.id)
    if not dto and not data_ref_user_id_data:
        text = await LangSet(call.from_user.id)._('id_not_found_error_text')
        await call.message.answer(text, reply_markup=await keyboard_check_is_registered(call.from_user.id))
        # await state.finish()
        return
    await state.finish()

    user_express_id = await db.get_express_id_by_user_id(call.from_user.id)
    if not user_express_id:
        user_express_id = await db.get_ref_users_id_by_user_id(call.from_user.id)
    id_1 = user_express_id['express_id']

    text_2 = await LangSet(call.from_user.id)._(
        'get_id_success_text_2')+ f"\n{id_1}\n" + f"""\n\n<code>收货人: {id_1}\n手机号码: 18161955318\n陕西省 西安市 雁塔区 丈八沟街道  高新区丈八六路49号103室中京仓库\n({id_1})\nPOSTCODE: 710076</code>
"""
    # 'get_id_success_text_2') + f"\n\n<code>收货人：阿龙\n电话：13777324343\n收货地址：广东省佛山市南海区里水镇河塱沙中庄中兴街11号菜鸟驿站\n{id_1}</code>"

    await call.message.answer(text_2)
    await call.message.delete()
    # await call.message.answer(text_3, reply_markup=await express_id_btn2(call.from_user.id))


@dp.message_handler(KeyboardFilter(keys='btn_main_4'), state=None)
async def btn_main_1(message: types.Message, state: FSMContext):
    await state.finish()
    dto = await db.get_express_id_by_user_id(message.from_user.id)
    if not dto:
        text = await LangSet(message.from_user.id)._('id_not_found_error_text')
        await message.answer(text, reply_markup=await keyboard_check_is_registered(message.from_user.id))
        # await state.finish()
        return
    text = await LangSet(message.from_user.id)._('question_text_choose')
    keys = await LangSet(message.from_user.id)._('buttons_questions')
    back_keys = await LangSet(message.from_user.id)._('back_button1')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton(value) for value in keys.values()]
    keyboard.add(*buttons)
    keyboard.row(back_keys)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(KeyboardFilter(keys='btn_abt_us_1'), state=None)
async def btn_abt_us_1(message: types.Message):
    text = await LangSet(message.from_user.id)._('about_us_text')
    return await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/topcargo_logo.png'),
        caption=text, reply_markup=await contact_us_buttons(message.from_user.id))


@dp.message_handler(KeyboardFilter(keys='btn_abt_us_2'), state=None)
async def btn_abt_us_2(message: types.Message):
    text = await LangSet(message.from_user.id)._('contact_us_text')
    return await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/topcargo_logo.png'),
        caption=text, reply_markup=await contact_us_buttons(message.from_user.id))


@dp.message_handler(KeyboardFilter(keys='btn_abt_us_3'), state=None)
async def btn_abt_us_3(message: types.Message):
    text = await LangSet(message.from_user.id)._('prohibited_products')
    return await message.answer_photo(
        photo=types.InputFile(path_or_bytesio='photos/topcargo_logo.png'),
        caption=text, reply_markup=await contact_us_buttons(message.from_user.id))
