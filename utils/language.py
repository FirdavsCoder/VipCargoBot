import json

from loader import db
from data.config import lang_file


class LangSet:
    def __init__(self, user_id):
        self.lang_file = lang_file
        self.user_id = user_id
        self.lang_dict = None

    async def _get_user_lang(self, user_id):
        res = await db.get_user_lang(user_id)
        self.lang_dict = res

    async def _(self, key):
        await self._get_user_lang(self.user_id)
        try:
            ret = self.lang_file[self.lang_dict][key]
        except KeyError:
            ret = self.lang_file['uz'][key]
        return ret

    async def select_lang(self):
        text = ''
        for lang in self.lang_file:
            text += lang_file[lang]['emoji'] + lang_file[lang]['select_lang'] + '\n'
        return text
