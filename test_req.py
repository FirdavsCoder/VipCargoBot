from datetime import datetime

import pandas as pd
import xlsxwriter
#
# # Fayl yo'lini kiriting
# file_path = './excel_files/ttt.xlsx'

# Excel faylni o'qiymiz
async def tashkent_complaints_send_func(file_name: str):
    now = datetime.now()
    output_file = f"output_{now.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    data = pd.read_excel(file_name, header=None)

    # Kerakli kodirovkalar ro'yxati
    valid_prefixes = ['TUS', 'TOP', 'TTZ', 'TQQ', 'TXO', 'TBO', 'TYN', 'TSM', 'TJZ', 'TGS', 'TAN', 'TFA', 'TNA']

    # Natija ma'lumotlarini saqlash uchun list
    result_data = []

    current_id_code = None
    for i in range(len(data)):
        cell_value = str(data.iloc[i, 0]).strip()  # 1-ustunni o'qiymiz

        # Agar katak bo'sh bo'lmasa va kerakli prefix bilan boshlansa, bu yangi `id_code`
        if any(cell_value.startswith(prefix) for prefix in valid_prefixes):
            current_id_code = cell_value

        # Track kod (raqam yoki harflar bilan aralash bo'lsa)
        elif current_id_code and cell_value:  # Bo'sh bo'lmagan qator
            result_data.append({'id_code': current_id_code, 'track_code': cell_value})

        print(current_id_code, cell_value)

    # Natijani yangi Excel faylga yozish
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Ustun nomlari
    worksheet.write(0, 0, 'id_code')
    worksheet.write(0, 1, 'track_code')

    # Ma'lumotlarni yozish
    for i, item in enumerate(result_data, start=1):
        worksheet.write(i, 0, item['id_code'])
        worksheet.write(i, 1, item['track_code'])

    # Workbookni yopamiz
    workbook.close()
    print("Excel fayl muvaffaqiyatli yaratildi:", output_file)

    return output_file
