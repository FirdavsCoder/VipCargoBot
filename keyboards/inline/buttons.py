from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import datetime


from utils.language import LangSet

file_name = "data.json"
with open(file_name, "r", encoding="utf-8") as file:
    regions_data = json.load(file)


async def admin_question_answer_keyboard(user_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="📝 Javob berish", callback_data=f"answer:{user_id}")
    )
    return markup


back_button_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_admin")
        ]
    ]
)


def generate_regions_keyboard():
    keyboard = InlineKeyboardMarkup()
    for region in regions_data:
        keyboard.add(InlineKeyboardButton(region['region'], callback_data=region['region']))
    return keyboard


def uzb_receive_btn(id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="To'lov qildim ✅", callback_data=f"delivery_product:{id}"),
                # InlineKeyboardButton(text="📦 O'zim olib kelaman", callback_data="take_away")
            ]
        ]
    )

    return keyboard


delivered_success_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Dostavka uchun ariza berilgan ✅",
                callback_data="success_delivery_request"
            )
        ]
    ]
)

take_away_success_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="O'zim olib keldim ✅",
                callback_data="success_take_away"
            )
        ]
    ]
)


def admin_delivered_btn(payment_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yuborildi ✅", callback_data=f"successfully_takeout_box:{payment_id}"),
                InlineKeyboardButton(text="Bekor qilindi ❌", callback_data=f"canceled_takeout_box:{payment_id}")
            ],
            [
                InlineKeyboardButton(text="To'lov qabul qilindi ✅",
                                     callback_data=f"successfully_payment_delivered_box:{payment_id}"),
            ]
        ]
    )
    return keyboard


def admin_delivered_btn_2(user_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yuborildi ✅", callback_data=f"successfully_takeout_box:{user_id}"),
                InlineKeyboardButton(text="Bekor qilindi ❌", callback_data=f"canceled_takeout_box:{user_id}")
            ],
        ]
    )
    return keyboard


# admin_delivered_canceled_product_btn = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Yuborildi ✅", callback_data="successfully_takeout_box"),
#             InlineKeyboardButton(text="Bekor qilindi ❌", callback_data="canceled_takeout_box")
#         ],
#         [
#             InlineKeyboardButton(text="To'lov qabul qilindi ✅", callback_data=f"successfully_payment_takeout_box:{user_id}"),
#         ]
#     ]
# )


async def discount_button(user_id):
    text = await LangSet(user_id)._('discount_btn_text')
    link = await LangSet(user_id)._('discount_btn_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


def complaint_answer_button(user_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Javob berish", callback_data=f"complaint_answer_btn:{user_id}")
            ]
        ]
    )
    return markup


async def keyboard_check_is_registered(user_id):
    text = await LangSet(user_id)._('button_text_inline')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, callback_data="register_user")
        ]
    ])
    return keyboard


async def check_track_code_button_use_credentials(user_id):
    link = await LangSet(user_id)._('chinese_track_code_check_link')
    text = await LangSet(user_id)._('chinese_track_code_check_2')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def uzb_track_code_check_button(user_id):
    link = await LangSet(user_id)._('uzb_track_code_edit_text')
    text = await LangSet(user_id)._('uzb_track_code_button_text')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def success_express_prognoz_button(user_id):
    link = await LangSet(user_id)._('prognoz_success_btn_text_link')
    text = await LangSet(user_id)._('prognoz_success_btn_text')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def last_price_button1(user_id):
    link = await LangSet(user_id)._('last_price_button1_link')
    text = await LangSet(user_id)._('last_price_button1')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def last_price_button2(user_id):
    link = await LangSet(user_id)._('last_price_button2_link')
    text = await LangSet(user_id)._('last_price_button2')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def express_id_btn1(user_id):
    text = await LangSet(user_id)._('success_express_id_button_text')
    link = await LangSet(user_id)._('success_express_id_button_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def express_id_btn2(user_id):
    text = await LangSet(user_id)._('success_express_id_button2_text')
    link = await LangSet(user_id)._('success_express_id_button2_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def know_address_button(user_id):
    text = await LangSet(user_id)._('id_exist_error_button')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, callback_data="know_id_address")
        ]
    ])
    return keyboard


async def button_cargo_id_btn(user_id):
    text = await LangSet(user_id)._('cargo_id_button_text')
    link = await LangSet(user_id)._('cargo_id_button_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def question_quickly_btn(user_id):
    text = await LangSet(user_id)._('question_text_button_choose_text')
    link = await LangSet(user_id)._('question_text_button_choose_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def support_btn(user_id):
    text = await LangSet(user_id)._('support_button_text')
    link = await LangSet(user_id)._('support_button_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def paid_success_btn():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="To'lov qildim ✅", callback_data='paid_success')
        ]
    ])
    return keyboard


async def yes_or_new_enter_button_for_delivery_products_data():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha, yana shu ✅", callback_data="callback_delivery_yes"),
            InlineKeyboardButton(text="Yangi kiritaman 📝", callback_data="callback_delivery_new")
        ]
    ])
    return keyboard


async def keyboard_check_is_registered(user_id):
    text = await LangSet(user_id)._('button_text_inline')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, callback_data="register_user")
        ]
    ])
    return keyboard


async def support_btn(user_id):
    text = await LangSet(user_id)._('support_button_text')
    link = await LangSet(user_id)._('support_button_link')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, url=link)
        ]
    ])
    return keyboard


async def choose_mail_type_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟡 Yandex", callback_data="yandex"),
                InlineKeyboardButton(text="🟣 Emu", callback_data="emu")
            ],
            [
                InlineKeyboardButton(text="🔵 BTS", callback_data="bts"),
                InlineKeyboardButton(text="🟠 O'zim olib ketaman", callback_data="ozim_olib_ketaman")
            ]
        ]
    )
    return keyboard



async def choose_mail_type_tch_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟡 Yandex", callback_data="yandex"),
                InlineKeyboardButton(text="🟠 O'zim olib ketaman", callback_data="ozim_olib_ketaman")
            ],
            [
                InlineKeyboardButton(text='🟣 Emu', callback_data="emu"),
            ]
        ]
    )
    return keyboard





# Inline tugmalar funksiyasi
def get_inline_keyboard():
    # Hozirgi sana
    today = datetime.datetime.now()

    # Hozirgi oy (strftime('%m.%Y') avtomatik ravishda oy raqamini ikki xonali qiladi)
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

