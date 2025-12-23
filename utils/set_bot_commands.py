from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand('link', 'VIP clientlar uchun faqat'),
            types.BotCommand('lang', 'Tilni o\'zgartirish'),
            types.BotCommand('admin', '[ONLY ADMINS] Admin panel'),
            types.BotCommand('panel', '[ONLY TEACHERS] Kuratorlar uchun'),
        ]
    )
