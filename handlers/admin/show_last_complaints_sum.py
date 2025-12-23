from pyexpat.errors import messages

from data.config import SUPER_ADMINS, OTCHET_CHANNEL
from keyboards.inline.admin_btns import admin_menu
from loader import dp, db, bot
from aiogram import types


@dp.callback_query_handler(text="last_complaints_sum")
async def last_complaints_sum(call: types.CallbackQuery):
    if call.from_user.id in SUPER_ADMINS:
        complaints = await db.get_last_complaints_sum()
        print("ACHCHOTLAR : \n\n\n",complaints, "\n\n\n\n")
        text = ""
        if not complaints:
            text = "Hozircha hech qanday achchotlar mavjud emas!"
        else:
            previous_location = None  # Oldingi locationni saqlash uchun

            for i in complaints:
                try:
                    total_sum_formatted = f"{i['total_sum']:,}".replace(',', '.')

                    # Agar location o'zgarayotgan bo'lsa, 2 ta yangi qatordan keyin yozish
                    if previous_location != i['location']:
                        if previous_location is not None:  # Birinchi marta kelganda qo'shmaslik uchun
                            text += "\n\n"
                        text += f"{i['location']}:\n"

                    text += f"{i['type_product']} - {i['total_weight']} kg - {total_sum_formatted} SO'M\n"
                    previous_location = i['location']  # Locationni yangilash
                except Exception as err:
                    print(err)

        # print(complaints[0]['total_sum'])
        # print()


        await call.message.answer(text)
        try:
            if call.from_user.id != 1849953640:
                await bot.send_message(
                    chat_id=OTCHET_CHANNEL,
                    text=text
                )
        except Exception as err:
            await call.message.answer("Xatolik yuz berdi! ERROR: ", err)
            print(err)

        await call.answer()
        return
    else:
        await call.answer("BU FUNKSIYA FAQAT SUPER ADMINLAR UCHUN!", show_alert=True)
        return