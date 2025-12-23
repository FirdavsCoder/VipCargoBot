from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

teacher_dashboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("🔗 Referral linki", callback_data="get_ref_link"),
            InlineKeyboardButton("📊 Statistika", callback_data="get_statistics")
        ],
        [
            InlineKeyboardButton("💰 Balance", callback_data="get_balance"),
            InlineKeyboardButton("⚙️ Sozlamalar", callback_data="settings_teacher")
        ]
    ]
)

withdraw_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("💳 Pulni olish", callback_data="withdraw_my_money"),
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_dashboard"),
        ]
    ]
)

yes_or_no_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha, to'g'ri ✅", callback_data="yes_right"),
            InlineKeyboardButton(text="Yo'q, noto'g'ri ❌", callback_data="no_wrong")
        ]
    ]
)

settings_menu_teacher = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Karta Malumotlarini o'zgartirish", callback_data="edit_card_datas"),
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_dashboard"),
        ]
    ]
)

question_payment = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Ha ✅", callback_data="pay_request"),
            InlineKeyboardButton("Yo'q ❌", callback_data="cancel_request")
        ]
    ]
)


def teacher_payment_success_btn_markup(teacher_id):
    teacher_payment_success_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("✅ To'lov qilindi", callback_data=f"payment_success:{teacher_id}"),
                InlineKeyboardButton("❌ To'lov bekor qilindi", callback_data=f"payment_cancel:{teacher_id}")
            ]
        ]
    )
    return teacher_payment_success_btn
