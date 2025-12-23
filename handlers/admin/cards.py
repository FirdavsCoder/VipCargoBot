import re

from aiogram.types import InlineKeyboardMarkup

from data.config import ADMINS, SUPER_ADMINS
from filters.keyboard_filter import IsSuperAdmin
from handlers.admin.admin import load_admins
from keyboards.inline.admin_btns import admin_menu
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from states.states import AddCardState


async def generate_cards_inline_buttons(cards):
    buttons = InlineKeyboardMarkup(row_width=2)
    if cards:
        for card in cards:
            buttons.insert(types.InlineKeyboardButton(text=card['card_number'], callback_data=f"card_{card['id']}"))
    buttons.row(types.InlineKeyboardButton(text="➕ Karta qo'shish", callback_data="add_card"))
    buttons.row(types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_menu"))
    return buttons

async def back_menu_admin():
    buttons = InlineKeyboardMarkup()
    buttons.row(types.InlineKeyboardButton(text="🔙 Orqaga", callback_data="admin_menu"))
    return buttons

@dp.callback_query_handler(text='admin_menu', state='*')
async def admin_menu_func(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Admin menyusi", reply_markup=await admin_menu(call.from_user.id))
    await state.finish()
    await call.answer()
    return

@dp.callback_query_handler(text='add_card')
async def add_card(call: types.CallbackQuery):
    await call.message.edit_text("16 talik karta raqamini kiriting, qanday kiritsanfiz shunday ko'rinadi userlarga ham!", reply_markup=await back_menu_admin())
    await AddCardState.card_number.set()

@dp.message_handler(state=AddCardState.card_number)
async def add_card(message: types.Message, state: FSMContext):
    check_card_number_regex = r"^\d{16}$"
    if not re.match(check_card_number_regex, message.text):
        await message.answer("Karta raqamini noto'g'ri kiritdingiz. Iltimos 16 ta raqamni bo'sh joylarsiz kiriting", reply_markup=await back_menu_admin())
        return
    card_number = message.text
    await state.update_data(card_number=card_number)
    await AddCardState.next()
    await message.answer("Karta nomini kiriting:", reply_markup=await back_menu_admin())

@dp.message_handler(state=AddCardState.card_name)
async def add_card(message: types.Message, state: FSMContext):
    branch = ''
    card_name = message.text
    data = await state.get_data()
    card_number = data.get('card_number')
    formatted_card_number_each_four_number_space = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
    admin_data = await db.get_branch_data_by_admin_id(message.from_user.id)
    if admin_data:
        branch = admin_data['branch_code']
        await db.insert_card(card_number=formatted_card_number_each_four_number_space, card_name=card_name,
                             branch_code=branch)
        await message.answer("Karta muvaffaqiyatli qo'shildi", reply_markup=await back_menu_admin())
        await state.finish()
    elif not admin_data and message.from_user.id not in ADMINS:
        await message.answer("Siz admin emassiz!")
        await state.finish()
        return
    elif message.from_user.id in SUPER_ADMINS:
        await message.answer("Branch kodini kiriting: ", reply_markup=await back_menu_admin())
        await state.update_data(card_name=card_name)
        await AddCardState.card_branch_code.set()
        return



@dp.message_handler(state=AddCardState.card_branch_code)
async def get_branch_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    card_branch_code = message.text
    branch_data = await db.get_branch_channel_by_branch_code(card_branch_code)
    if len(card_branch_code) == 3 and branch_data:
        card_number = data.get('card_number')
        card_name = data.get('card_name')
        await db.insert_card(card_number=card_number, card_name=card_name, branch_code=card_branch_code)
        await message.answer("Karta muvaffaqiyatli qo'shildi", reply_markup=await back_menu_admin())
        await state.finish()
    else:
        await message.answer("Branch topilmadi", reply_markup=await back_menu_admin())
        await state.finish()









@dp.callback_query_handler(text='cards')
async def cards_func(call: types.CallbackQuery):
    global cards
    ext = "Kartalaringiz:\n\n"
    branch_data = await db.get_branch_data_by_admin_id(call.from_user.id)
    if call.from_user.id in SUPER_ADMINS:
        cards = await db.get_all_cards()
    elif branch_data:
        cards = await db.get_all_cards_by_branch_code(branch_data['branch_code'])
    if cards:
        for card in cards:
            ext += f"🔴 {card['card_number']}\n{card['card_name']} | {card['branch_code']}\n\n"
        await call.message.edit_text(text=ext, reply_markup=await generate_cards_inline_buttons(cards))
    else:
        await call.message.edit_text("Kartalar topilmadi", reply_markup=await generate_cards_inline_buttons(cards))

    await call.answer()
    return


@dp.callback_query_handler(text_contains='card_')
async def card_func(call: types.CallbackQuery):
    card_id = int(call.data.split('_')[-1])
    card = await db.get_card_by_id(card_id)
    await db.delete_card_by_id(card_id)
    await call.answer(f"🔴 {card['card_number']}\n{card['card_name']} karta o'chirildi!")
    ext = "Kartalaringiz:\n\n"
    cards = await db.get_all_cards()
    if cards:
        for card in cards:
            ext += f"🔴 {card['card_number']}\n{card['card_name']}\n\n"
        await call.message.edit_text(text=ext, reply_markup=await generate_cards_inline_buttons(cards))
    else:
        await call.message.edit_text("Kartalar topilmadi", reply_markup=await generate_cards_inline_buttons(cards))
    await call.answer()
    return