from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.config import lang_file
from loader import db


async def language_keyboard(user_id):
    lang = await db.get_user_lang(user_id)
    k = []
    markup = InlineKeyboardMarkup(row_width=1)
    for key in lang_file:
        text = lang_file[key]['emoji'] + lang_file[key]['nativeName']
        if lang == key:
            text += '✅'
        k.append(InlineKeyboardButton(
            text=text,
            callback_data='language_' + key))
    markup.add(*k)
    return markup


