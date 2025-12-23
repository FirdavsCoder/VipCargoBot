import os

from check import id_excel_writer
from loader import db, dp, bot
from aiogram import types
from filters.keyboard_filter import IsSuperAdmin


@dp.callback_query_handler(IsSuperAdmin(), text='get_id_excel')
async def express_id_excel(call: types.CallbackQuery):
    try:
        await call.answer()
        msg_id = (await call.message.answer('Bajarilyapti...\n\n'
                                            'Iltimos kuting malumotlar kopligi '
                                            'uchun bu uzoqroq vaqt olishi mumkin...')).message_id
        data = await db.get_all_express_id()
        # print(1)
        # print(data)
        file_name = await id_excel_writer(data)


        await bot.delete_message(chat_id=call.message.chat.id, message_id=msg_id)
        await call.message.answer_document(document=open(file_name, 'rb'),
                                           caption="ID EXCEL")
        #
        # print(3)

        # file = types.InputFile(path_or_bytesio=f"./express_id.xlsx")
        # await bot.send_document(call.from_user.id, file, caption="Express ID")
        # await call.answer()
        os.remove(file_name)
    except Exception as err:
        await call.answer('Hali Express Prognoz fayliga yozilgan malumotlar mavjud emas.', show_alert=True)
