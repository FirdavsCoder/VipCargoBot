import asyncio

import pandas as pd

from keyboards.inline.buttons import uzb_receive_btn
from loader import db, bot
from utils.language import LangSet
from utils.text_formatter import text_formatter


# async def read_excel(
#         file_name: str,
#         receive_china: bool = False,
#         receive_tashkent: bool = False
# ):
#     price = await db.get_price(type='avia_express')
#     price2 = await db.get_price(type='auto_express')
#     global data, text, data_id
#     df = pd.read_excel(f"./excel_files/{file_name}")
#
#     for index, row in df.iterrows():
#         user_id_code = row['id_code']
#         track_code = row['track_code']
#         weight = row['weight']
#         type_product = str(row['TYPE'])
#         track_code_status = await db.check_track_code(str(track_code))
#         if not track_code_status:
#             await db.insert_track_codes(
#                 user_id_code,
#                 str(track_code),
#                 weight,
#                 receive_china=receive_china,
#                 receive_uz=receive_tashkent,
#                 type=type_product
#             )
#         else:
#             if receive_china:
#                 await db.update_track_status_china_receive(str(track_code))
#                 # await
#             elif receive_tashkent:
#                 await db.update_track_status_receive_uz(str(track_code))
#         data_user = await db.get_user_id_by_express_id(user_id_code)
#         # for i in data:
#         try:
#             if type(track_code) == int:
#                 track_code = str(track_code)
#
#                 response = await db.check_uzb_track_code(track_code=track_code)
#                 text = f"\n<b>Trek kodi:</b> <code>{track_code}</code>"
#                 try:
#                     if response['receive_uz']:
#                         data_id = (await bot.send_message(
#                             chat_id=data_user['user_id'],
#                             text=text_formatter(
#                                 text=text,
#                                 weight=weight,
#                                 price=price['price'],
#                                 price2=price2['price'],
#                                 receive_china=response['receive_china'],
#                                 receive_uz=response['receive_uz'],
#                                 type=type_product
#                             ),
#                             # reply_markup=uzb_receive_btn()
#                         )).message_id
#                     else:
#                         data_id = (
#                             await bot.send_message(
#                                 chat_id=data_user['user_id'],
#                                 text=text_formatter(
#                                     text=text,
#                                     weight=weight,
#                                     price=price['price'],
#                                     price2=price2['price'],
#                                     receive_china=response['receive_china'],
#                                     receive_uz=response['receive_uz'],
#                                     type=type_product
#                                 ),
#                             )).message_id
#                 except Exception as e:
#                     print(e)
#                     if response['receive_uz']:
#                         try:
#                             data_id = (
#                                 await bot.send_message(
#                                     chat_id=data_user['user_id'],
#                                     text=text_formatter(
#                                         text=text,
#                                         weight=weight,
#                                         price=price['price'],
#                                         price2=price2['price'],
#                                         receive_china=response['receive_china'],
#                                         receive_uz=response['receive_uz'],
#                                         type=type_product
#                                     ),
#                                     # reply_markup=uzb_receive_btn()
#                                 )).message_id
#                         except Exception as e:
#                             print(e)
#                             pass
#                     else:
#                         try:
#                             data_id = (
#                                 await bot.send_message(
#                                     chat_id=data_user['user_id'],
#                                     text=text_formatter(
#                                         text=text,
#                                         weight=weight,
#                                         price=price['price'],
#                                         price2=price2['price'],
#                                         receive_china=response['receive_china'],
#                                         receive_uz=response['receive_uz'],
#                                         type=type_product
#                                     ), )).message_id
#                         except Exception as e:
#                             print(e)
#                             pass
#                 await bot.pin_chat_message(data_user['user_id'], data_id)
#         except Exception as e:
#             print(e)
#             pass


async def read_excel_achchot(file_name: str):
    global user_data, data_payment_info
    df = pd.read_excel(f"./excel_files/{file_name}")
    for index, row in df.iterrows():
        try:
            id_code = row['ID']
            kg = row['KG']
            date = row['Sana']
            product_count = row['Tovar Soni']
            price = row['NARX']
            user_data = await db.get_user_id_by_express_id(express_id=str(id_code))

            try:

                data_payment_info = await db.add_uzb_delivered_payment(
                    user_id=int(user_data[1]),
                    id_code=str(id_code),
                    kg=str(kg),
                    price=str(price),
                    date=str(date),
                    product_count=str(product_count),
                    photo_link='https://t.me/uzbexpress/2'
                )
            except Exception as e:
                await bot.send_message(chat_id=1849953640, text=f"Databazaga qo'shishda xatolik: {e}")
                pass
            user_id = user_data[1]
            caption = f"""
👩🏻‍💻 Hurmatli Mijoz：

<b>ID Code:</b> {id_code}
<b>Vazni:</b> {kg}
<b>Narxi:</b> {price}
<b>Sana:</b> {str(date)}
<b>Tovar soni:</b> {product_count}

📦 Yukingiz Omborimizga yetib keldi.

👩🏻‍💻 Iltimos, 48 soat ichida to'lovni amalga oshiring va quyidagi tugmani bosib to'lov qilganingizni tasdiqlovchi chekni bizga yuboring. 

💳 <code>1234 5678 9123 4123</code>
👤 Falonchi Falonchi

⚠️ To'lov qilingan yuklar 15 kun omborimizda bepul saqlanadi va 2 oy davomida musodara qilinmaydi. Aksincha, to'lov qilinmagan yuklar musodara bo'lish yoki yo'qolish xavfi bor.
        """
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=caption,
                    reply_markup=uzb_receive_btn(data_payment_info)
                )
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass


async def read_excel_ref_user_achchot(file_name: str):
    global user_data, data_payment_info
    df = pd.read_excel(f"./ref_user_files/{file_name}")
    print(df)
    for index, row in df.iterrows():
        try:
            id_code = row['ID']
            kg = row['KG']
            date = row['Sana']
            product_count = row['Tovar Soni']
            price = row['NARX']
            print(id_code)
            user_data = await db.get_user_id_by_ref_users_id(express_id=str(id_code))
            print(1)
            print(user_data['express_id'][:3])
            try:
                data_teacher = await db.get_teacher_data_by_express_code(express_code=user_data['express_id'][:3])
                print(2)
                print(data_teacher)
                mention = await bot.get_chat(user_data['user_id'])
                update_sum = int(kg) * float(data_teacher['price'])
                text_teacher = (f"🎉 <i><b>Balansingiz <u>{update_sum}$</u> ga to'ldirildi!</b></i>\n"
                                f"💰 Balansingizda: <u>{update_sum+float(data_teacher['balance'])}$</u>"
                                "\n\n"
                                f"📦 Siz taklif {mention.get_mention()} ning {kg} kg yuki keldi!")
                print(update_sum)
                await db.update_ref_link_balance(user_id=data_teacher['user_id'], balance=str(update_sum+float(data_teacher['balance'])))
                await bot.send_message(
                    chat_id=data_teacher['user_id'],
                    text=text_teacher,
                    parse_mode='HTML'
                )
                data_payment_info = await db.add_uzb_delivered_payment(
                    user_id=int(user_data[1]),
                    id_code=str(id_code),
                    kg=str(kg),
                    price=str(price),
                    date=str(date),
                    product_count=str(product_count),
                    photo_link='https://t.me/uzbexpress/2'
                )
            except Exception as e:
                await bot.send_message(chat_id=1849953640, text=f"Databazaga qo'shishda xatolik: {e}")
                pass
            user_id = user_data[1]
            caption = f"""
👩🏻‍💻 Hurmatli Mijoz：

<b>ID Code:</b> {id_code}
<b>Vazni:</b> {kg}
<b>Narxi:</b> {price}
<b>Sana:</b> {str(date)}
<b>Tovar soni:</b> {product_count}

📦 Yukingiz Omborimizga yetib keldi.

👩🏻‍💻 Iltimos, 48 soat ichida to'lovni amalga oshiring va quyidagi tugmani bosib to'lov qilganingizni tasdiqlovchi chekni bizga yuboring. 

💳 <code>1234 5678 9123 4123</code>
👤 Falonchi Falonchi

⚠️ To'lov qilingan yuklar 15 kun omborimizda bepul saqlanadi va 2 oy davomida musodara qilinmaydi. Aksincha, to'lov qilinmagan yuklar musodara bo'lish yoki yo'qolish xavfi bor.
        """
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=caption,
                    reply_markup=uzb_receive_btn(data_payment_info)
                )
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass







##################
###########################
######################################



async def read_excel_easy(
        file_name: str,
        time: str = '19:00',
        receive_china: bool = False,
        receive_tashkent: bool = False
):
    global data, text, data_id
    df = pd.read_excel(f"{file_name}")

    for index, row in df.iterrows():
        user_id_code = row['id_code']
        track_code = row['track_code']
        track_code_status = await db.check_track_code(str(track_code))
        print(track_code_status)
        if not track_code_status:
            await db.insert_track_codes(
                user_id_code,
                str(track_code),
                receive_china=receive_china,
                receive_uz=receive_tashkent,
                type='Avia'
            )
        else:
            if receive_china:
                await db.update_track_status_china_receive(str(track_code))
                # await
            elif receive_tashkent:
                await db.update_track_status_receive_uz(str(track_code))
        data_user = await db.get_user_id_by_express_id(user_id_code)
        print(data_user)
        # for i in data:
        try:
            print('track code type: ', type(track_code))
            if type(track_code) == int:
                print('KIRDI IFGA INT:   ', track_code)
                track_code = str(track_code)
                # print(track_code)

                response = await db.check_uzb_track_code(track_code=track_code)
                text = f"\n<b>Trek kodi:</b> <code>{track_code}</code>"

                if response['receive_uz']:
                    data_id = (await bot.send_message(
                        chat_id=data_user['user_id'],
                        text=text_formatter(
                            text=text,
                            time=time,
                            receive_china=response['receive_china'],
                            receive_uz=response['receive_uz']
                        ),
                        # reply_markup=uzb_receive_btn()
                    )).message_id
                else:
                    data_id = (
                        await bot.send_message(
                            chat_id=data_user['user_id'],
                            text=text_formatter(
                                text=text,
                                time=time,
                                receive_china=response['receive_china'],
                                receive_uz=response['receive_uz'],
                            ),
                        )).message_id

                await bot.pin_chat_message(data_user['user_id'], data_id)
                await asyncio.sleep(0.33)
            elif type(track_code) == str:
                print('KIRDI IFGA STRRRRRR:  ', track_code)
                response = await db.check_uzb_track_code(track_code=track_code)
                text = f"\n<b>Trek kodi:</b> <code>{track_code}</code>"

                if response['receive_uz']:
                    data_id = (await bot.send_message(
                        chat_id=data_user['user_id'],
                        text=text_formatter(
                            text=text,
                            time=time,
                            receive_china=response['receive_china'],
                            receive_uz=response['receive_uz']
                        ),
                        # reply_markup=uzb_receive_btn()
                    )).message_id
                else:
                    data_id = (
                        await bot.send_message(
                            chat_id=data_user['user_id'],
                            text=text_formatter(
                                text=text,
                                time=time,
                                receive_china=response['receive_china'],
                                receive_uz=response['receive_uz'],
                            ),
                        )).message_id

                await bot.pin_chat_message(data_user['user_id'], data_id)
                await asyncio.sleep(0.33)
            print("KIRMADI IFGA:   ", track_code)
        except Exception as e:
            print(e)
            pass


async def read_excel_track_codes(
        file_name: str,
        reys_name: str,
):
    print(file_name)
    df = pd.read_excel(f"{file_name}")
    for index, row in df.iterrows():
        receive_date = row['收货日期']
        track_code = row['货件追踪代码']
        product_name = row['Название товара']
        count = row['数量']
        weight = row['重量/KG']
        print(type(receive_date))
        print("RECEIVE DATE: ", receive_date)
        print("TRACK CODE: ", track_code)
        print("PRODUCT NAME: ", product_name)
        print("COUNT: ", count)
        print("WEIGHT: ", weight)
        print(track_code)
        track_code_status = await db.check_track_code_base(str(track_code))
        if not track_code_status:
            print(1)
            await db.insert_track_codes_base(
                track_code=str(track_code),
                weight=weight,
                count=count,
                product_name=product_name,
                reys_name=reys_name,
                receive_date=str(receive_date)
            )









