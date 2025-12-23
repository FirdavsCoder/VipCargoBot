import os
from datetime import datetime

from filters.keyboard_filter import IsSuperAdmin
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from states.states import ChineseWarehouseReceive
from test_req import tashkent_complaints_send_func
from utils.excel_read import read_excel_easy


# Excel READ Chinese Warehouse Receive
@dp.callback_query_handler(IsSuperAdmin(), text='chinese_warehouse_receive')
async def chinese_warehouse_receive(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.answer("Excel faylini yuboring. Iltimos to'g'ri fayl yuklayoganingizni tekshiring.")
        await ChineseWarehouseReceive.file.set()
        await state.update_data(receive_china=True)
        await state.update_data(receive_tashkent=False)
        await call.answer()
    except Exception as err:
        await call.answer('Hali Chinese Warehouse Receive fayliga yozilgan malumotlar mavjud emas.', show_alert=True)


@dp.callback_query_handler(IsSuperAdmin(), text='tashkent_warehouse_receive')
async def chinese_warehouse_receive(call: types.CallbackQuery, state: FSMContext):
    try:
        # await call.message.answer("Excel faylini yuboring. Iltimos to'g'ri fayl yuklayoganingizni tekshiring.")
        # await ChineseWarehouseReceive.file.set()
        await ChineseWarehouseReceive.time.set()
        await state.update_data(out_china=False)
        await state.update_data(receive_china=False)
        await state.update_data(receive_tashkent=True)
        await call.answer()
        await call.message.answer("Soatni kiriting. Misol uchun 10:00")
    except Exception as err:
        await call.answer('Hali Chinese Warehouse Receive fayliga yozilgan malumotlar mavjud emas.', show_alert=True)


@dp.message_handler(IsSuperAdmin(), state=ChineseWarehouseReceive.time)
async def chinese_warehouse_receive_time(message: types.Message, state: FSMContext):
    time = message.text
    await state.update_data(time=time)
    await message.answer("Soat qabul qilindi. Endi excel faylni yuboring.")
    await ChineseWarehouseReceive.file.set()


@dp.message_handler(IsSuperAdmin(), state=ChineseWarehouseReceive.file, content_types=types.ContentType.DOCUMENT)
async def chinese_warehouse_receive_file(message: types.Message, state: FSMContext):
    data = await state.get_data()
    china_in = data['receive_china']
    receive_tashkent = data['receive_tashkent']
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    now = datetime.now()
    file_name = f"./excel_files/chinese_warehouse_receive_{now.strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"

    await file.download(destination_file=file_name)
    output_file = await tashkent_complaints_send_func(file_name)
    await state.update_data(file_path=output_file)
    if china_in:
        await read_excel_easy(
            time=data['time'],
            file_name=output_file,
            receive_china=True
        )
    elif receive_tashkent:
        await read_excel_easy(
            time=data['time'],
            file_name=output_file,
            receive_tashkent=True
        )
    await message.answer("Excel fayl yuklandi.")
    os.remove(file_name)
    os.remove(output_file)
    await state.finish()
