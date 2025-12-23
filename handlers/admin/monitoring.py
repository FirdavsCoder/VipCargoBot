import xlsxwriter
from aiogram import types
from my_calendar import get_inline_keyboard
from loader import db, dp, bot


# Ma'lumotlarni bazadan olish
async def fetch_data(date):
    # Mock data for testing
    data = await db.get_all_uzb_delivered_products_payment(date)
    print(data)
    return data


# Excel faylga yozish
def write_to_excel(data, total_revenue):
    workbook = xlsxwriter.Workbook('sales_data.xlsx')
    worksheet = workbook.add_worksheet()

    # Define cell formats
    header_format = workbook.add_format({
        'bold': True,
        'italic': True,
        'bg_color': '#D9EAD3',  # Light green background
        'border': 1
    })

    max_value_format = workbook.add_format({
        'bg_color': '#C6EFCD',  # Light green background
        'bold': True,
        'color': '#086F42'
    })

    min_value_format = workbook.add_format({
        'bg_color': '#FFC8CE',  # Light red background
        'bold': True,
        'color': '#A3343A'
    })

    cell_format = workbook.add_format({
        'border': 1
    })

    revenue_format = workbook.add_format({
        'bg_color': '#a6c2f5',  # Light red background
        'bold': True,
        'color': '#506ef2'
    })

    # Write headers
    worksheet.write(0, 0, 'ID', header_format)
    worksheet.write(0, 1, 'User ID', header_format)
    worksheet.write(0, 2, 'ID Code', header_format)
    worksheet.write(0, 3, 'KG', header_format)
    worksheet.write(0, 4, 'Date', header_format)
    worksheet.write(0, 5, 'Kategoriya', header_format)
    worksheet.write(0, 6, 'Price', header_format)
    worksheet.write(0, 7, 'Created At', header_format)

    row = 1
    for record in data:
        for col, value in enumerate(record):
            worksheet.write(row, col, value, cell_format)
        row += 1

        # Find the max and min values
    # max_value = max(data, key=lambda x: float(x[6].replace('.', '').replace(',', '')))
    # min_value = min(data, key=lambda x: float(x[6].replace('.', '').replace(',', '')))



    total_revenue = 0
    total_expenses = 0
    total_price = 0
    print(0)
    for record in data:
        try:
            print(record)
            print(1)
            price_str = str(record[6])  # Ensure the value is a string
            price = int(price_str.replace('.', ''))
            # Nuqtalarni olib tashlash va float ga o'tkazish
            # price_str = record[6].replace('.', '').replace(',', '')  # Nuqtalarni olib tashlash
            # price = int(price_str)  # Floyga o'tkazish
            total_price += price
            # Daromadlar va xarajatlarni ajratish
            if record[-1] == 'product_payments':  # Daromadlar
                total_revenue += price
            elif record[-1] == 'expenses':  # Xarajatlar
                total_expenses += price
                print(total_expenses)
        except (ValueError, TypeError):
            pass  # Agar xatolik bo'lsa, o'tib ketish
    print(2)

    # Excel faylga umumiy aylanmani yozish
    total_profit = total_revenue - total_expenses

    row += 2
    # Write max and min values
    worksheet.write(row, 0, f'Daromad:', max_value_format)
    worksheet.write(row, 1, total_revenue, max_value_format)
    row += 1
    worksheet.write(row, 0, f'Xarajat:', min_value_format)
    worksheet.write(row, 1, total_expenses, min_value_format)
    row += 1
    worksheet.write(row, 0, 'Jami aylanma:', revenue_format)
    worksheet.write(row, 1, total_price, revenue_format)



    # Diagrammani yaratish
    chart = workbook.add_chart({'type': 'pie'})

    # Diagrammaga ma'lumotlar qo'shish
    chart.add_series({
        'name': 'Oylik hisobot',
        'categories': ['Sheet1', 1, 0, row - 2, 0],
        'values': ['Sheet1', 1, 1, row - 2, 1],
        'data_labels': {'percentage': True},
    })

    chart.set_title({'name': 'Oylik hisobot'})

    # Diagrammani ishchi varaqqa qo'shish
    chart_position_row = row + 2
    worksheet.insert_chart('D{}'.format(chart_position_row), chart)
    row += 1
    #
    # # Write total revenue



    workbook.close()





@dp.callback_query_handler(text = "monitoring")
async def monitoring(call: types.CallbackQuery):
    await call.message.edit_text(
        text="Qaysi oyning hisobotini olmoqchisiz tanlang: ",
        reply_markup=get_inline_keyboard()
    )


@dp.callback_query_handler(text_contains = 'month')
async def choose_month_handler(call: types.CallbackQuery):
    month = call.data.split(':')[1]
    print('month', month)
    data = await fetch_data(month)
    if not data:
        await call.answer("Bu oyda malumotlar mavjud emas! Boshqa oyni tanlang!", cache_time=3, show_alert=True)
        return
    # Calculate total revenue
    total_revenue = 0
    for record in data:
        try:
            # Nuqtalarni olib tashlash va float ga o'tkazish
            price_str = str(record[6])  # Ensure the value is a string
            price_str = price_str.replace('.', '')  # Nuqtalarni olib tashlash
            total_revenue += float(price_str)  # Floyga o'tkazish
        except (ValueError, TypeError):
            pass  # Agar xatolik bo'lsa, o'tib ketish

    # Excel faylni yaratish
    write_to_excel(data, total_revenue)

    # Excel faylni yuborish
    with open('sales_data.xlsx', 'rb') as file:
        await bot.send_document(call.from_user.id, document=file)








