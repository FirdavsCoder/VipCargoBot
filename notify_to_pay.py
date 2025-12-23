import aioschedule
import asyncio

from data.config import CARD_NUMBER, CARD_OWNER
from keyboards.inline.buttons import uzb_receive_btn
from loader import bot, db
import functools
import datetime
from aiogram.utils.exceptions import BadRequest


async def send_function():
    users = await db.get_all_users_not_payed()
    for user in users:
        user_id = user['user_id']
        caption = f"""
👩🏻‍💻 Hurmatli Mijoz：

<b>ID:</b> {user['id_code']}
<b>Vazni:</b> {user['kg']}
<b>Narxi:</b> {user['price']}
<b>Sana:</b> {str(user['date'])}

📦 Yukingiz Omborimizga yetib keldi.

👩🏻‍💻 Iltimos, 48 soat ichida to'lovni amalga oshiring va quyidagi tugmani bosib to'lov qilganingizni tasdiqlovchi chekni bizga yuboring. 

💳 <code>{CARD_NUMBER}</code>
👤 {CARD_OWNER}

⚠️ 3 Kun ichida to’lov qilmasangiz 4chi kundan sizga jarima qo’llaniladi , 4chi kundan boshlab yukingizni har bir saqlangan kuni uchun 20.000 summdan jarima belgilanadi.
                                """
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=user['photo_link'],
                caption=caption,
                reply_markup=uzb_receive_btn(user['id'])
            )
            await asyncio.sleep(0.34)
        except Exception as e:
            print(e)
            pass


async def daily_tasks():
    job_func = functools.partial(send_function)
    aioschedule.every().day.at("22:00").do(job_func)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
