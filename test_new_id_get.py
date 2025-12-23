import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.default.buttons import get_regions_keyboard, data, get_branches_keyboard
from states.states import SelectionState

TOKEN = "6558566870:AAGxthz_yoVUoHovaKg78kUu2WkX9tJxUZ8"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())









# /start komandasi
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Iltimos, viloyatni tanlang:", reply_markup=get_regions_keyboard())
    await SelectionState.choosing_region.set()

# Viloyat tanlanganda
@dp.message_handler(state=SelectionState.choosing_region)
async def process_region(message: types.Message, state: FSMContext):
    region_name = message.text

    # Agar noto‘g‘ri viloyat tanlansa
    if region_name not in [list(item["region"].keys())[0] for item in data]:
        await message.answer("Iltimos, quyidagi viloyatlardan birini tanlang.", reply_markup=get_regions_keyboard())
        return

    await state.update_data(region=region_name)

    # Agar viloyatda tumanlar bo‘lsa
    for item in data:
        if region_name in item["region"]:
            if "branches" in item:
                await message.answer("Iltimos, tumanni tanlang:", reply_markup=get_branches_keyboard(region_name))
                await SelectionState.choosing_branch.set()
                return

    # Agar tumanlar bo‘lmasa, viloyat ID'sini yuboramiz
    region_code = [item["region"][region_name] for item in data if region_name in item["region"]][0]
    await message.answer(f"Tanlangan viloyat: {region_name}\nID: {region_code}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

# Tuman tanlanganda
@dp.message_handler(state=SelectionState.choosing_branch)
async def process_branch(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    region_name = user_data.get("region")

    if message.text == "⬅️ Orqaga":
        await message.answer("Iltimos, viloyatni tanlang:", reply_markup=get_regions_keyboard())
        await SelectionState.choosing_region.set()
        return

    for item in data:
        if region_name in item["region"] and "branches" in item:
            if message.text in item["branches"]:
                branch_code = item["branches"][message.text]
                await message.answer(f"Tanlangan tuman: {message.text}\nID: {branch_code}", reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
                return

    # Noto‘g‘ri tanlov bo‘lsa
    await message.answer("Iltimos, quyidagi tumanlardan birini tanlang.", reply_markup=get_branches_keyboard(region_name))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
