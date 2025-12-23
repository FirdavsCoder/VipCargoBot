import datetime

def text_formatter(
        text: str,
        time: str,
        receive_china: str,
        receive_uz: str

):
    print("TEXT FORMATTERGA KELDI")


    text += f"\n\n<b>Yo'nalish: </b> Avia"
    if receive_china:
        text += "\n\n<b>Xitoy omboriga qabul qilindi: </b> ✅"
    else:
        text += "\n\n<b>Xitoy omboriga qabul qilindi: </b> ⏳"

    if receive_uz:
        text += "\n\n<b>O'zbekistonga keldi: </b> ✅\n"
        text += f"\n⏰ Sana va vaqti: {time}"
    else:
        text += "\n\n<b>O'zbekistonga keldi: </b> ⏳"

    print("TEXT FORMATTERDAN QAYTDI")
    return text


def text_admin_express_id_formatter(
        express_id, data, filial):
    text = f"🆔 <b>Express ID:</b> {express_id}\n\n"
    text += f"📄 <b>Ism-Familiya:</b> {data['name']}\n"
    text += f"☎️ <b>Telefon raqami:</b> {data['phone_number']}\n"
    text += f"🔖 <b>Passport Seriya:</b> {data['passport_seria']}\n"
    text += f"🔢 <b>Passport PNFL:</b> {data['passport_info']}\n"
    text += f"📅 <b>Tugilgan sana:</b> {data['birthdate']}\n"
    text += f"📍 <b>Manzil:</b> {data['address']}\n"
    text += f"🏢 <b>Filial:</b> {filial}\n"
    print(text)
    return text

            # f"<b>Full name:</b> <i>{data['name']}</i>\n"
            # f"<b>Phone number:</b> <i>{data['phone_number']}</i>\n"
            # f"<b>Passport ID:</b> <i>{data['passport_seria']}</i>\n"
            # f"<b>Passport info:</b> <i>{data['passport_info']}</i>\n"
            # f"<b>Birthdate:</b> <i>{data['birthdate']}</i>\n"
            # f"<b>Address:</b> <i>{data['address']}</i>\n"
            # f"<b>Filial:</b> <i>{data['filial']}</i>\n")