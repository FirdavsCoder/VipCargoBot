import re
from datetime import datetime


def check_uzbekistan_passport(passport):
    pattern = r'^[A-Z]{2}\s*\d{7}$'
    if re.match(pattern, passport):
        return True
    else:
        return False


def is_valid_date(date_str):
    # Regex to match the date format DD.MM.YYYY
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'

    # Check if the date format matches the pattern
    if not re.match(pattern, date_str):
        return False

    # Extract the day, month, and year from the date string
    day, month, year = map(int, date_str.split('.'))

    # Check if the year is between 1960 and the current year
    current_year = datetime.now().year
    if not (1960 <= year <= current_year):
        return False

    # Check if the date is a valid calendar date
    try:
        datetime(year, month, day)
    except ValueError:
        return False

    return True


def is_valid_14_digit_number(number):
    # Regex to match exactly 14 digits
    pattern = r'^\d{14}$'
    return bool(re.match(pattern, number))


def is_valid_uzbekistan_phone_number(phone_number):
    pattern = r'^(\+998|998)[-\s]?\(?\d{2}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False


def is_valid_card_number(card_number):
    # Whitespace va tirelarni olib tashlash
    card_number = card_number.replace(" ", "").replace("-", "")

    # Faqat 16 raqamli bo'lishini tekshirish
    if re.fullmatch(r'\d{16}', card_number):
        return True
    else:
        return False
