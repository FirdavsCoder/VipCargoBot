import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




# Inline tugmalar funksiyasi
def get_inline_keyboard():
    # Hozirgi sana
    today = datetime.datetime.now()

    # Hozirgi oy
    current_month = today.strftime('%m.%Y')

    # 1 va 2 oy oldin
    one_month_ago = (today.replace(day=1) - datetime.timedelta(days=1)).strftime('%m.%Y')
    two_months_ago = (today.replace(day=1) - datetime.timedelta(days=32)).strftime('%m.%Y')

    # Inline tugmalar yaratish
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton(text=current_month, callback_data=f"month:{current_month}"),
        InlineKeyboardButton(text=one_month_ago, callback_data=f"month:{one_month_ago}"),
        InlineKeyboardButton(text=two_months_ago, callback_data=f"month:{two_months_ago}")
    )
    return keyboard

