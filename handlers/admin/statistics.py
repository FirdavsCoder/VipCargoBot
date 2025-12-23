import asyncio
from datetime import datetime

from keyboards.inline.admin_btns import admin_menu
# from keyboards.inline.buttons import admin_panel_button, back_button_inline
from loader import db, dp, bot
from aiogram import types
from filters.keyboard_filter import IsSuperAdmin


@dp.callback_query_handler(IsSuperAdmin(), text='statistics')
async def statistics(call: types.CallbackQuery):
    all_user = await db.all_user_count()
    date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    today_added_users = await db.count_today_added_users()
    week_added_users = await db.count_week_added_users()
    month_added_users = await db.count_month_added_users()

    text = f'📊 Statistika\n\n👥 Umumiy foydalanuvchilar soni: <b>{all_user}</b>\n'
    text += f"⏰ Oxirgi 12 soatda qo'shilgan foydalanuvchilar: <b>{await db.last12hour_added_users()}</b>\n"
    text += f"📅 Bugun qo\'shilgan foydalanuvchilar: <b>{today_added_users}</b>\n"
    text += f"⏳ Bu haftada qo\'shilgan foydalanuvchilar: <b>{week_added_users}</b>\n\n"
    text += f"{await db.compute_percent()}\n"
    text += f"🗒 Bu oyda qo'shilgan foydalanuvchilar: <b>{month_added_users}</b>\n\n"

    # text += "<b>EXPRESS PROGNOZLAR</b>\n"
    # text += f'👥 Umumiy Express Prognozlar soni: <b>{await db.all_express_prognoz_count()}</b>\n'
    # text += f"⏰ Oxirgi 12 soatda qo'shilgan Express Prognozlar: <b>{await db.last12hour_added_prognoz()}</b>\n"
    # text += f"📅 Bugun qo\'shilgan Express Prognozlar: <b>{await db.count_today_added_prognoz()}</b>\n"
    # text += f"⏳ Bu haftada qo\'shilgan Express Prognozlar: <b>{await db.count_week_added_prognoz()}</b>\n"
    # text += f"🗒 Bu oyda qo'shilgan Express Prognozlar: <b>{await db.count_month_added_prognoz()}</b>\n\n"
    # #
    # text += "<b>CARGO PROGNOZLAR</b>\n"
    # text += f'👥 Umumiy Cargo Prognozlar soni: <b>{await db.all_cargo_prognoz_count()}</b>\n'
    # text += f"⏰ Oxirgi 12 soatda qo'shilgan Cargo Prognozlar: <b>{await db.last12hour_added_cargo_prognoz()}</b>\n"
    # text += f"📅 Bugun qo\'shilgan Cargo Prognozlar: <b>{await db.count_today_added_cargo_prognoz()}</b>\n"
    # text += f"⏳ Bu haftada qo\'shilgan Cargo Prognozlar: <b>{await db.count_week_added_cargo_prognoz()}</b>\n"
    # text += f"🗒 Bu oyda qo'shilgan Cargo Prognozlar: <b>{await db.count_month_added_cargo_prognoz()}</b>\n\n"
    #
    # text += "<b>CARGO ID lar</b>\n"
    # text += f'👥 Umumiy Cargo ID lar soni: <b>{await db.all_cargo_id_count()}</b>\n'
    # text += f"⏰ Oxirgi 12 soatda qo'shilgan Cargo ID lar: <b>{await db.last12hour_added_cargo_id()}</b>\n"
    # text += f"📅 Bugun qo\'shilgan Cargo ID lar: <b>{await db.count_today_added_cargo_id()}</b>\n"
    # text += f"⏳ Bu haftada qo\'shilgan Cargo ID lar: <b>{await db.count_week_added_cargo_id()}</b>\n"
    # text += f"🗒 Bu oyda qo'shilgan Cargo ID lar: <b>{await db.count_month_added_cargo_id()}</b>\n\n"

    text += "<b>EXPRESS ID lar</b>\n"
    text += f'👥 Umumiy Express ID lar soni: <b>{await db.all_express_id_count()}</b>\n'
    text += f"⏰ Oxirgi 12 soatda qo'shilgan Express ID lar: <b>{await db.last12hour_added_express_id()}</b>\n"
    text += f"📅 Bugun qo\'shilgan Express ID lar: <b>{await db.count_today_added_express_id()}</b>\n"
    text += f"⏳ Bu haftada qo\'shilgan Express ID lar: <b>{await db.count_week_added_express_id()}</b>\n"
    text += f"🗒 Bu oyda qo'shilgan Express ID lar: <b>{await db.count_month_added_express_id()}</b>\n\n"

    text += f'\n📅 {date_time}'
    await call.answer()
    # print(text)
    await call.message.edit_text(text, reply_markup=await admin_menu(call.from_user.id))
