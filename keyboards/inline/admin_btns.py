from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


async def admin_menu(user_id: int):
    data_admin = await db.get_branch_data_by_admin_id(user_id)
    if data_admin:
        markup = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📈 Statistika", callback_data="statistics"),
                ],
                [
                    InlineKeyboardButton(text="🤖 Avto отчет", callback_data="auto_achchot_send"),
                ],
                [
                    InlineKeyboardButton(text="💳 Kartalar", callback_data="cards")
                ]
            ])
    else:
        markup = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [
                    # InlineKeyboardButton(text="🇨🇳 Xitoyga kirdi", callback_data="chinese_warehouse_receive"),
                    InlineKeyboardButton(text="📤 Reklama yuborish", callback_data="send_ad"),
                    InlineKeyboardButton(text="🇺🇿 Toshkentga kirdi", callback_data="tashkent_warehouse_receive"),
                    InlineKeyboardButton(text="TRACK Code EXCEL", callback_data="track_code_excel"),
                    # InlineKeyboardButton(text="📋 Bittalik achchot", callback_data="one_achchot")
                ],
                # [
                #     InlineKeyboardButton(text="📝 Achchotlar", callback_data="complaints_sending"),
                #     InlineKeyboardButton(text="🖇 Achchotlar Referal", callback_data="complaints_sending_ref_users"),
                # ],
                [
                    # InlineKeyboardButton(text="📊 ID Excel", callback_data="get_id_excel"),
                    # InlineKeyboardButton(text="📤 Reklama yuborish", callback_data="send_ad")
                ],
                [
                    InlineKeyboardButton(text="📈 Statistika", callback_data="statistics"),
                    InlineKeyboardButton(text="🔗 Referal ssilka yaratish", callback_data="create_ref_link"),
                ],
                [
                    InlineKeyboardButton(text="1️⃣ Bittalik отчет", callback_data="one_achchot_send"),
                    InlineKeyboardButton(text="🤖 Avto отчет", callback_data="auto_achchot_send"),
                ],
                [
                    InlineKeyboardButton(text="💳 Kartalar", callback_data="cards")
                ],
                [
                    InlineKeyboardButton(text="📊 Oxirgi achchot summasi", callback_data='last_complaints_sum')
                ],
                # [
                #     InlineKeyboardButton(text="📊 Monitoring", callback_data='monitoring')
                # ]
            ])
    return markup
async def branch_admin_menu():
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📈 Statistika", callback_data="statistics"),
            ],
            [
                InlineKeyboardButton(text="🤖 Avto отчет", callback_data="auto_achchot_send"),
            ],
            [
                InlineKeyboardButton(text="💳 Kartalar", callback_data="cards")
            ]
        ])
    return markup

def check_express_id_btn(data_id, msg_id, user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilindi",
                                     callback_data=f"accepted_express_id:{data_id}:{user_id}"),
                InlineKeyboardButton(text="❌ Bekor qilindi",
                                     callback_data=f"cancelled_express_id:{data_id}:{msg_id}:{user_id}")
            ]
        ]
    )
    return markup


def check_ref_user_id_btn(data_id, msg_id, user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Qabul qilindi",
                                     callback_data=f"accepted_ref_user_id:{data_id}:{user_id}"),
                InlineKeyboardButton(text="❌ Bekor qilindi",
                                     callback_data=f"cancelled_ref_user_id:{data_id}:{msg_id}:{user_id}")
            ]
        ]
    )
    return markup


def uzb_receive_btn(id_payment):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="To'lov qildim ✅", callback_data=f"delivery_product:{id_payment}"),
                # InlineKeyboardButton(text="📦 O'zim olib kelaman", callback_data="take_away")
            ]
        ]
    )

    return keyboard


def type_one_achchot_send():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Oddiy tovar", callback_data="type_choose_one_ODDIY_tovar"),
                InlineKeyboardButton(text="GABARIT TOVAR", callback_data="type_choose_one_GABARIT_tovar"),
            ],
            [
                InlineKeyboardButton(text="Seriya tovar", callback_data="type_choose_one_SERIYA_tovar"),
                InlineKeyboardButton(text="BREND TOVAR", callback_data="type_choose_one_BREND_tovar"),
            ],
            [
                InlineKeyboardButton(text="SKIDKA 9.5$", callback_data="type_choose_one_ODDIY10KG+_tovar"),
            ]
        ]
    )
    return keyboard


def type_auto_achchot_send():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Oddiy tovar", callback_data="type_choose_one_ODDIY_tovar"),
                InlineKeyboardButton(text="ODDIY YUK SKIDKA 9$", callback_data="type_choose_one_ODDIY10KG+_tovar"),
            ],
            [
                InlineKeyboardButton(text="Seriya tovar", callback_data="type_choose_one_SERIYA_tovar"),
                InlineKeyboardButton(text="BREND TOVAR", callback_data="type_choose_one_BREND_tovar"),
            ],
            [
                InlineKeyboardButton(text="AVTO TOVAR", callback_data="type_choose_one_AVTO_tovar"),
            ]
        ]
    )
    return keyboard


def type_expense_choose():
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍔 Oziq-ovqat", callback_data="type_expense_choose_ovqat"),
                InlineKeyboardButton(text="💰 Oylik", callback_data="type_expense_choose_oylik"),
                InlineKeyboardButton(text="📦 Boshqa", callback_data="type_expense_choose_boshqa"),
            ]
        ]
    )
    return markup

