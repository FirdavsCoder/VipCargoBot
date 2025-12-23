import asyncio

import pandas as pd
import functools

from loader import bot, db


async def id_Excel_read():
    df = pd.read_excel(f"./id_base/excel2.xlsx")

    for index, row in df.iterrows():
        user_id = row['user_id']
        first_name_last_name = row['fio']
        id_code = row['id']
        passport_seriya = row['passport']
        manzil = row['manzil']
        tel_raqam = row['tel']
        PINIFIL = row['pinfl']

        text = (
            f"User_id: {user_id}\n"
            f"FIO: {first_name_last_name}\n"
            f"ID: {id_code}\n"
            f"PASSPORT: {passport_seriya}\n"
            f"MANZIL: {manzil}\n"
            f"TEL: {tel_raqam}\n"
            f"PINIFIL: {PINIFIL}\n"
        )

        await bot.send_message(
            chat_id=1849953640,
            text=text
        )
        await bot.send_message(
            chat_id=6954395758,
            text=text
        )

        await db.add_express_id2(
            user_id=int(user_id),
            full_name=first_name_last_name,
            express_id=id_code,
            passport_seria=passport_seriya,
            address=manzil,
            phone_number=str(tel_raqam),
            passport_pnfl=str(PINIFIL)
        )
        await asyncio.sleep(0.3)


