import os
import xlsxwriter

import pandas as pd
from datetime import datetime


async def id_excel_writer(data: list):
    # df = pd.DataFrame(data)
    # print(1.1)
    # today_date = datetime.today().strftime('%Y-%m-%d')
    # file_name = f'id_excel{today_date}.xlsx'
    # print(file_name)
    # print(1.2)
    # df.to_excel(file_name, index=False)
    # print(1.3)

    # Hozirgi sanani olish
    today_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f'database_data_{today_date}.xlsx'

    # Excel faylini yaratish
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    # Sarlavhalarni yozish
    headers = ['id', 'user_id', 'express_id', 'full_name', 'region', 'passport_id', 'phone_number', 'created_at']
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    # Ma'lumotlarni yozish
    for row_num, record in enumerate(data, 1):
        worksheet.write(row_num, 0, record['id'])
        worksheet.write(row_num, 1, record['user_id'])
        worksheet.write(row_num, 2, record['express_id'])
        worksheet.write(row_num, 3, record['full_name'])
        worksheet.write(row_num, 4, record['region'])
        worksheet.write(row_num, 5, record['passport_id'])
        worksheet.write(row_num, 6, record['phone_number'])
        worksheet.write(row_num, 7, record['created_at'].strftime('%Y-%m-%d %H:%M:%S'))

    # Excel faylni saqlash va yopish
    workbook.close()

    return file_name
