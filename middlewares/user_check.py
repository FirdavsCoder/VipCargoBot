import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db, bot
from utils.language import LangSet
from keyboards.inline.language_keyboard import language_keyboard


class UserCheckMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(UserCheckMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        type = message.chat.type
        if type == 'private':
            check_user = await db.get_user_by_id(message.from_user.id)
            if check_user:
                pass
            if not check_user:
                await db.add_user(message.from_user.id)
                text = await LangSet(message.from_user.id)._('please_select_lang')
                await message.answer(text=text, reply_markup=await language_keyboard(message.from_user.id))
                args = message.get_args()
                if args:
                    data = await db.get_ref_link_by_link_code(args)
                    if data:
                        dto = await db.get_referral_user_by_user_id(user_id=message.from_user.id)
                        if not dto:
                            await bot.send_message(
                                chat_id=data['user_id'],
                                text=f"🎉 Sizning taklifingiz bilan yangi foydalanuvchi ro'yxatdan o'tdi.\n"
                                     f"👤 Ismi: {message.from_user.get_mention()}\n"
                                     f"🔗 Taklif linki: {args}"
                            )
                            await db.add_referral_user(
                                user_id=message.from_user.id,
                                teacher_id=data['user_id'],
                                name=message.from_user.full_name,
                                express_code=data['express_code'],
                                link_code=args
                            )
                raise CancelHandler()
