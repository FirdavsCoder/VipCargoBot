from loader import db
from utils.language import LangSet
from data.config import lang_file
from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import ADMINS


class KeyboardFilter(BoundFilter):
    def __init__(self, keys: str):
        self.keys = keys

    async def check(self, message: types.Message):
        lang = await db.get_user_lang(message.from_user.id)
        if not lang:
            lang = 'uz'
        if self.keys == 'back_button1':
            if message.text == lang_file[lang]['back_button1']:
                return True
        elif self.keys == 'savol_button':
            if message.text == lang_file[lang]['savol_button']:
                return True
        else:
            try:
                lang_set = LangSet(message.from_user.id)
                button = await lang_set._(self.keys)
                if message.text in button.values():
                    return True
                else:
                    return False
            except Exception as e:
                print(f"Exception in ckhr: {e}")
                return False


class Private(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class Channel(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.CHANNEL


class Group(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.SUPERGROUP


class IsSuperAdmin(BoundFilter):
    # print("Ishladi...")

    async def check(self, message: types.Message):
        user_id = message.from_user.id

        if user_id in ADMINS:
            return True
        else:
            return False



class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        user_id = int(message.from_user.id)
        if user_id in ADMINS:
            return True
        else:
            return False
