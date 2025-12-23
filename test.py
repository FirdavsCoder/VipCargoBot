import xlsxwriter
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6630543950:AAH3p_Xf15-0YO7FJwV_pRqqy06A7STOR50'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchi kiritgan ma'lumotlarni saqlash uchun
data = []
labels = []


# Start komandasiga javob
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Diagramma uchun ma'lumotlarni kiriting (masalan: olma 10, banan 20)")


# Ma'lumotlarni qabul qilish
@dp.message_handler()
async def collect_data(message: types.Message):
    global data, labels
    try:
        # Foydalanuvchi kiritgan ma'lumotlarni ajratish
        entries = message.text.split(',')
        for entry in entries:
            label, value = entry.split()
            labels.append(label)  # Meva nomi (label)
            data.append(int(value))  # Raqamli qiymat

        await message.reply(f"Ma'lumotlar qabul qilindi: {list(zip(labels, data))}")

        # Excel fayliga dumaloq diagramma yaratish
        create_pie_chart(data, labels)
        await message.reply("Excel fayl yaratildi va dumaloq diagramma chizildi.")

        # Faylni foydalanuvchiga yuborish
        with open('pie_chart.xlsx', 'rb') as file:
            await bot.send_document(message.chat.id, file)
    except ValueError:
        await message.reply("Iltimos, ma'lumotlarni to'g'ri kiriting (masalan: olma 10, banan 20).")

def create_pie_chart(data, labels):
    # Excel fayl yaratish
    workbook = xlsxwriter.Workbook('pie_chart.xlsx')
    worksheet = workbook.add_worksheet()

    # Ma'lumotlarni Excel faylga yozish
    worksheet.write_column('A1', labels)
    worksheet.write_column('B1', data)

    # Dumaloq diagramma yaratish
    chart = workbook.add_chart({'type': 'pie'})

    # Ranglar ro'yxati (och ranglar)
    colors = ['#FF9999',  # Och pushti
              '#99FF99',  # Och yashil
              '#9999FF',  # Och ko'k
              '#FFFF99',  # Och sariq
              '#FF99FF',  # Och pushti binafsha
              '#99FFFF']  # Och moviy

    # Diagramma uchun ma'lumotlar ko'rsatish va ranglarni belgilang
    chart.add_series({
        'categories': '=Sheet1!$A$1:$A$' + str(len(data)),
        'values':     '=Sheet1!$B$1:$B$' + str(len(data)),
        'points':     [{'fill': {'color': colors[i]}} for i in range(len(data))],  # Ranglar har bir segment uchun
        'data_labels': {
            'percentage': True,  # Foizlarni ko'rsatish
            'value': True,       # Miqdorlarni ko'rsatish
            'separator': '\n',   # Miqdor va foizni yangi qatorda ko'rsatish
            'number_format': '#,##0" so\'m"'  # Miqdordan keyin "so'm" qo'shish va formatlash
        }
    })

    # Diagrammaga sarlavha qo'shish
    chart.set_title({'name': 'Kirim chiqim statistika'})

    # Diagrammani joylashtirish
    worksheet.insert_chart('D1', chart)

    # Excel faylni saqlash
    workbook.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
