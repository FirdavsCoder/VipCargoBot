from data.config import VIP_WEIGHT
from loader import db

async def check_user_flight_status(user_id: int):
    rows = await db.check_user_flight_is_vip(user_id)
    over_8kg = [float(row['total_kg']) > VIP_WEIGHT for row in rows]
    if not over_8kg or not over_8kg[0]:
        return None
    count = sum(over_8kg)
    if count == 1:
        return """\
    Tabriklaymiz! 🎉

Sizning birinchi 3 kiloli buyurtmangiz muvaffaqiyatli amalga oshdi!

Yana 2marta 3 kg buyurtma qilsangiz, sizga bepul WeChat kursi va qo‘shimcha 500+ WeChat kontaktlar taqdim etiladi.Keyingi buyurtmalaringizda omad tilaymiz!

Top Cargo bilan tez va qulay yetkazib berish!

—-

Поздравляем! 🎉

Ваш первый заказ на 3 кг успешно выполнен!

Сделайте ещё 2 заказа по 3 кг, и вы получите бесплатный курс по WeChat и дополнительно 500+ WeChat контактов.
Желаем удачи в следующих заказах!

Быстрая и удобная доставка с Top Cargo!"""
    elif count == 2:
        return """\
    Zo‘r ishlayapsiz! 👏

Endi sizning ikkinchi 3 kiloli buyurtmangiz ham muvaffaqiyatli bajarildi!
Atigi bitta 3 kg yuk buyurtma qilsangiz, WeChat kursi + 500+ kontaktlar sizniki bo‘ladi!

Top Cargo – sifatli va tezkor xizmat!

—-

Отличная работа! 👏

Ваш второй заказ на 3 кг также успешно выполнен!
Сделайте всего ещё один заказ на 3 кг, и курс по WeChat + 500+ контактов будут вашими!

Top Cargo – качественный и быстрый сервис!"""
    elif count == 3:
        await db.update_express_id_is_vip_by_user_id(user_id, True)
        return """\
    Tabriklaymiz! 🎊

Sizning uchinchi 3 kg buyurtmangiz ham muvaffaqiyatli amalga oshdi!
Va’da qilinganidek, sizga WeChat kursi va 500+ kontaktlar taqdim etildi!

Ushbu havolaga kirib bemalol tekin darslikdan foydalanishingiz mumkun 👉🏻 https://t.me/+C-ZiTjsmFdplMGEy

Hurmatli mijoz, biz bilan birga bo‘lganingiz uchun rahmat!
Hurmat bilan - Top Cargo 🚀

——

Поздравляем! 🎊

Ваш третий заказ на 3 кг также успешно выполнен!
Как и обещали, мы предоставили вам курс по WeChat и 500+ контактов!

Перейдите по этой ссылке и воспользуйтесь бесплатным курсом 👉🏻 https://t.me/+C-ZiTjsmFdplMGEy

Уважаемый клиент, спасибо, что вы с нами!
С уважением – Top Cargo 🚀"""
    return None

