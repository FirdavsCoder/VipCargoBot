from aiogram import types

from utils.language import LangSet
import json

file_name = "data.json"
with open(file_name, "r", encoding="utf-8") as file:
    regions_data = json.load(file)


async def start_menu(user_id: int):
    keys = await LangSet(user_id)._('button_start')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keys_list = list(keys.values())
    if keys_list:
        keyboard.row(keys_list[0])
    for i in range(1, len(keys_list), 2):
        if i + 1 < len(keys_list):
            keyboard.row(keys_list[i], keys_list[i + 1])
        else:
            keyboard.row(keys_list[i])
    return keyboard


async def back_button(user_id: int):
    back_keys = await LangSet(user_id)._('back_button1')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    keyboard.row(back_keys)
    return keyboard


async def generate_regions_keyboard_button(user_id):
    back_keys = await LangSet(user_id)._('back_button1')
    keyboard = types.ReplyKeyboardMarkup()
    for region in regions_data:
        keyboard.add(types.KeyboardButton(region['region']))
    keyboard.row(back_keys)
    return keyboard


async def check_your_get_id_data(user_id):
    back_keys = await LangSet(user_id)._('back_button1')
    check_btn = await LangSet(user_id)._('check_text')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(check_btn)
    keyboard.row(back_keys)
    return keyboard


async def contact_us_buttons(user_id):
    back_keys = await LangSet(user_id)._('back_button1')
    keys = await LangSet(user_id)._('about_us_buttons')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keys_list = list(keys.values())
    if keys_list:
        keyboard.row(keys_list[0])
    for i in range(1, len(keys_list), 2):
        if i + 1 < len(keys_list):
            keyboard.row(keys_list[i], keys_list[i + 1])
        else:
            keyboard.row(keys_list[i])
    keyboard.row(back_keys)
    return keyboard


file_name = "branches_data.json"
with open(file_name, "r", encoding="utf-8") as file:
    data = json.load(file)



# Viloyatlar uchun ReplyKeyboard yaratish
def get_regions_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data:
        region_name = list(item["region"].keys())[0]
        keyboard.add(types.KeyboardButton(region_name))
    return keyboard

# Tumanlar uchun ReplyKeyboard yaratish
def get_branches_keyboard(region_name):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in data:
        if region_name in item["region"]:
            if "branches" in item:
                for branch in item["branches"].keys():
                    keyboard.add(types.KeyboardButton(branch))
                keyboard.add(types.KeyboardButton("⬅️ Orqaga"))
    return keyboard