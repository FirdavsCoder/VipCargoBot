from keyboards.default.buttons import start_menu
from keyboards.inline.language_keyboard import language_keyboard
import logging
from aiogram import types
from loader import dp, db, bot
from utils.language import LangSet
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['lang'])
async def set_lang(message: types.Message):
    if message.chat.type == 'private':
        text = await LangSet(message.from_user.id)._('please_select_lang')
        await message.answer(text=text, reply_markup=await language_keyboard(message.from_user.id))


@dp.callback_query_handler(lambda c: c.data.startswith('language_'))
async def set_lang(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split('_')[1]
    res = await db.get_user_by_id(user_id)
    if res:
        language = str(res['lang'])
        logging.info(f'User {user_id} set language {lang}')
        await db.update_lang(lang, user_id)
        await callback_query.answer(await LangSet(user_id)._('set_lang'))
        if language != lang:
            text1 = await LangSet(user_id)._('start')
            await callback_query.message.answer(text1, reply_markup=await start_menu(callback_query.from_user.id))
            await callback_query.message.delete()
        else:
            await db.update_lang(lang, user_id)
            text1 = await LangSet(user_id)._('start')
            await callback_query.message.answer(text1, reply_markup=await start_menu(callback_query.from_user.id))
            await callback_query.message.delete()
        if language == "False":
            text = await LangSet(user_id)._('start')
            await callback_query.message.answer(text)
    else:
        await db.update_lang(lang, user_id)
        text1 = await LangSet(user_id)._('start')
        await callback_query.message.answer(text1, reply_markup=await start_menu(callback_query.from_user.id))
        await callback_query.message.delete()
