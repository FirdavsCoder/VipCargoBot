from loader import bot, db, dp
from aiogram import types

from utils.language import LangSet


@dp.callback_query_handler(text_contains='accepted_ref_user_id')
async def accepted_express_id(call: types.CallbackQuery):
    print(call.data)
    data_id = call.data.split(":")[1]
    dto = await db.get_ref_users_id_by_id(int(data_id))
    print(dto)
    await db.update_ref_user_id_status(int(data_id), status="accepted")
    txt = await LangSet(int(call.data.split(":")[2]))._('copy_text')
    text1 = await LangSet(int(call.data.split(":")[2]))._('id_text1') + f"\n\n🛩️ 🆔 Avia Cargo ID: {dto['express_id']}\n"
    text1 += f"""<code>
收货人: {dto['express_id']}
手机号码: 18161955318
陕西省 西安市 雁塔区 丈八沟街道  高新区丈八六路49号103室中京仓库
({dto['express_id']})</code> {txt}

Avia post code: 710076
"""
    await bot.send_message(call.data.split(":")[2], text1)
    screen_txt = await LangSet(int(call.data.split(":")[2]))._('check_your_Address_get_id')
    await bot.send_photo(
        chat_id=call.data.split(":")[2],
        photo=types.InputFile(path_or_bytesio='photos/check_address_screenshot.jpg'),
        caption=screen_txt
    )
    last_txt = await LangSet(int(call.data.split(":")[2]))._('admin_send_photo_get_id')
    if dto['express_id'].startswith('TNA'):
        txt = last_txt.replace("@manager_topcargo", f"@topcargo_namangan_admin")
        await bot.send_message(call.data.split(":")[2], txt)
    else:
        await bot.send_message(call.data.split(":")[2], last_txt)
    await call.message.delete()
    await call.answer("✅ Qabul qilindi", show_alert=True)


@dp.callback_query_handler(text_contains='cancelled_ref_user_id')
async def cancelled_express_id(call: types.CallbackQuery):
    print(call.data)
    data_id = call.data.split(":")[1]
    print(data_id)
    await db.delete_ref_user_id(int(data_id))
    await bot.delete_message(call.message.chat.id, call.data.split(":")[2])
    await bot.delete_message(call.message.chat.id, int(call.data.split(":")[2]) + 1)
    text = await LangSet(int(call.data.split(":")[3]))._('reject_id_text')
    new_txt = text.replace("#son", f"#{data_id}")
    await bot.send_message(call.data.split(":")[3], new_txt)
    await call.answer("❌ Bekor qilindi", show_alert=True)
    await call.message.delete()
