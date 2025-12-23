import logging
import xlsxwriter
import matplotlib.pyplot as plt
from io import BytesIO
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loader import bot, db

API_TOKEN = '6630543950:AAH3p_Xf15-0YO7FJwV_pRqqy06A7STOR50'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Ma'lumotlarni bazadan olish
async def fetch_data():
    # Mock data for testing
    data = await db.get_all_uzb_delivered_products_payment()
    return data


def create_chart(data):
    categories = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Create a figure with two subplots (one row, two columns)
    fig, axs = plt.subplots(1, 2, figsize=(18, 8))  # Adjust the figure size as needed

    # Pie chart
    wedges, texts, autotexts = axs[0].pie(
        counts,
        labels=categories,
        autopct='%1.1f%%',
        colors=plt.get_cmap('Pastel1').colors,
        shadow=True,
        startangle=140
    )
    axs[0].set_title('Oylik hisobot (Pie Chart)')
    axs[0].set_aspect('equal')  # Ensure pie chart is circular

    # Enhance readability
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_color('black')

    # Bar chart
    axs[1].bar(categories, counts, color=plt.get_cmap('Pastel1').colors)
    axs[1].set_title('Oylik hisobot (Bar Chart)')
    axs[1].set_xlabel('Category')
    axs[1].set_ylabel('Count')

    # Improve layout
    plt.tight_layout()

    # Save the figure to BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return buf

# Excel faylga yozish
def write_to_excel(data):
    workbook = xlsxwriter.Workbook('sales_data.xlsx')
    worksheet = workbook.add_worksheet()

    # Define cell formats
    header_format = workbook.add_format({
        'bold': True,
        'italic': True,
        'bg_color': '#D9EAD3',  # Light green background
        'border': 1
    })

    cell_format = workbook.add_format({
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

    # Write headers
    worksheet.write(0, 0, 'Category', header_format)
    worksheet.write(0, 1, 'Count', header_format)

    row = 1
    for category, count in data:
        worksheet.write(row, 0, category, cell_format)
        worksheet.write(row, 1, count, cell_format)
        row += 1

    # Find the max and min values
    max_value = max(data, key=lambda x: x[1])
    min_value = min(data, key=lambda x: x[1])

    row += 2
    # Write max and min values
    worksheet.write(row, 0, f'Daromad:', max_value_format)
    worksheet.write(row, 1, max_value[1], max_value_format)
    row += 1
    worksheet.write(row, 0, f'Xarajat:', min_value_format)
    worksheet.write(row, 1, min_value[1], min_value_format)

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

    workbook.close()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Iltimos, /report buyrug'ini yuboring.")


@dp.message_handler(commands=['report'])
async def send_report(message: types.Message):
    data = fetch_data()

    # Diagrammani yaratish
    chart_buffer = create_chart(data)

    # Excel faylni yaratish
    write_to_excel(data)

    # Diagrammani yuborish
    chart_buffer.seek(0)  # Ensure buffer position is at the start
    await bot.send_photo(message.chat.id, photo=chart_buffer)

    # Excel faylni yuborish
    with open('sales_data.xlsx', 'rb') as file:
        await bot.send_document(message.chat.id, document=file)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
