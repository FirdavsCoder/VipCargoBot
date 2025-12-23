import json
from aiogram import types

file_name = "data.json"
with open(file_name, "r", encoding="utf-8") as file:
    regions_data = json.load(file)

region_map = {
    'Namangan viloyati': 'TNA',
    'Fargona viloyati': 'TFA',
    'Andijon viloyati': 'TAN',
    'Sirdaryo viloyati': 'TGS',
    'Jizzax viloyati': 'TJZ',
    'Samarqand viloyati': 'TSM',
    'Navoiy viloyati': 'TYN',
    'Buxoro viloyati': 'TBO',
    'Xorazm viloyati': 'TXO',
    'Qashqadaryo viloyati': 'TQQ',
    'Surxondaryo viloyati': 'TTZ',
    'Qoraqalpogiston Respublikasi': 'TUS',
    'Toshkent viloyati': 'TOP',
    'Toshkent shahri': 'TOP',
}

async def generate_regions_keyboard_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for region in regions_data:
        keyboard.add(types.KeyboardButton(region['region']))
    return keyboard


async def generate_branch_keyboard(region_name):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    selected_region = next((r for r in regions_data if r["region"] == region_name), None)

    if not selected_region:
        return keyboard.add(types.KeyboardButton("Region topilmadi ❌"))

    region_code = region_map.get(region_name, "N/A")

    for district in selected_region["districts"]:
        branch_code = f"{region_code}-{district[:3].upper()}"  # Masalan: TOP-CHI (Toshkent - Chilonzor)
        keyboard.add(types.KeyboardButton(f"{district} ({branch_code})"))

    return keyboard


from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: Message):
    keyboard = await generate_regions_keyboard_button()
    await message.answer("Viloyatni tanlang:", reply_markup=keyboard)

@dp.message_handler()
async def region_handler(message: Message):
    region_name = message.text
    keyboard = await generate_branch_keyboard(region_name)
    await message.answer(f"{region_name} uchun filiallarni tanlang:", reply_markup=keyboard)

executor.start_polling(dp)
