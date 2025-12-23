from aiogram.dispatcher import FSMContext

from keyboards.default.buttons import back_button
from keyboards.inline.admin_btns import type_expense_choose, admin_menu
from loader import dp, db, bot
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from states.states import AddExpenseState


@dp.callback_query_handler(text="add_expense")
async def add_expense(call: types.CallbackQuery):
    await call.message.answer("Rasxod qo'shish uchun summani kiriting:\n<b>Masalan: 80000</b>", reply_markup=await back_button(call.from_user.id))
    await AddExpenseState.amount.set()


@dp.message_handler(state=AddExpenseState.amount)
async def get_amount(message: types.Message, state: FSMContext):
    amount = message.text
    await state.update_data(amount=amount)
    await message.answer("Xarajat qaysi turda ekanligini tanlang: ", reply_markup=type_expense_choose())
    await message.answer("Tanlang 👆", reply_markup=await back_button(message.chat.id))
    await AddExpenseState.next()


@dp.callback_query_handler(state=AddExpenseState.type)
async def get_type(call: CallbackQuery, state: FSMContext):
    type = call.data.split("_")[3]
    data = await state.get_data()
    await db.add_expense(amount=int(data.get("amount")), type=type)
    await call.message.answer("Rasxod muvaffaqiyatli qo'shildi!", reply_markup=await admin_menu(call.from_user.id))
    await state.finish()
