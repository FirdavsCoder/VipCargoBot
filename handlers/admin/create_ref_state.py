from keyboards.default.buttons import start_menu, back_button
from loader import bot, dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.states import CreateRefState


@dp.callback_query_handler(text_contains='create_ref_link')
async def create_ref_link(call: types.CallbackQuery):
    await CreateRefState.user_id.set()
    await call.message.answer("Foydalanuvchi Telegram-ID raqamini kiriting", reply_markup=await back_button(call.from_user.id))
    await call.answer()


@dp.message_handler(state=CreateRefState.user_id)
async def create_ref_link(message: types.Message, state: FSMContext):
    user_id = message.text
    data = await db.get_user_by_id(int(user_id))
    if not data:
        await message.answer("Bunday foydalanuvchi mavjud emas!", reply_markup=await back_button(message.from_user.id))
        return
    dto = await db.get_ref_link_by_user_id(int(user_id))
    if dto:
        await message.answer("Bu foydalanuvchiga avvalgiroq ssilka yaratilgan!", reply_markup=await back_button(message.from_user.id))
        return
    await state.update_data(user_id=user_id)
    await CreateRefState.next()
    await message.answer("Kuratorning ismini kiriting: ", reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=CreateRefState.name)
async def create_ref_link(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await CreateRefState.next()
    await message.answer("Kuratorni ssilka kodini kiriting: ", reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=CreateRefState.link_code)
async def create_ref_link(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(link_code=name)
    await CreateRefState.next()
    await message.answer("Kuratorni id-code shtrixini kiriting: ", reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=CreateRefState.express_code)
async def create_ref_link(message: types.Message, state: FSMContext):
    code = message.text
    await state.update_data(express_code=code)
    await CreateRefState.next()
    await message.answer("Kurator bilan kelishilgan narxni kiriting: ", reply_markup=await back_button(message.from_user.id))


@dp.message_handler(state=CreateRefState.price)
async def create_ref_link(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    try:
        bot_data = await bot.get_me()
        link = 'https://t.me/' + bot_data.username + '?start=' + str(data['link_code'])
        print(link)
        await db.create_ref_link(
            user_id=int(data.get('user_id')),
            name=data.get('name'),
            link_code=data.get('link_code'),
            express_code=data.get('express_code'),
            price=data.get('price'),
            link=link
        )
        data_msg_id = (await bot.send_message(
            chat_id=int(data.get('user_id')),
            text=f"😊 Assalomu alaykum hurmatli <b>{data.get('name')}</b>!\n "
                 f"<i>Siz botimizda kurator bo'ldingiz. 🎉</i>\n\n"
                 f"📝 <i>Sizning ssilka kodingiz:</i> <b>{data.get('link_code')}</b>\n"
                 f"🪪 <i>Sizning id-code shtrixingiz:</i> <b>{data.get('express_code')}</b>\n"
                 f"💵 <i>Siz bilan kelishilgan narxi:</i> <b>{data.get('price')}$</b>\n"
                 f"🔗 <i>Sizning ssilka manzilingiz:</i>\n{link}\n\n"
                 f"📌 <i>Siz kuratorni boshqaruv paneliga /panel komandasi orqali o'tishingiz mumkin.</i>"
        )).message_id
        await bot.pin_chat_message(
            chat_id=int(data.get('user_id')),
            message_id=data_msg_id
        )
    except Exception as e:
        print(e)
        await message.answer(f"Xatolik yuz berdi: {e}")
        return
    await message.answer("Sizning ma'lumotlaringiz muvaffaqiyatli saqlandi! ✅",
                         reply_markup=await start_menu(message.from_user.id))
    await state.finish()
