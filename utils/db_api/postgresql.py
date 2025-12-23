from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # async def add_user(self, user_id, full_name, region, cargo_id, passport_id, phone_number, lang: str = 'ru'):
    #     sql = "INSERT INTO users (user_id, full_name, region, cargo_id, passport_id, phone_number, lang) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
    #     return await self.execute(sql, user_id, full_name, region, cargo_id, passport_id, phone_number, lang,
    #                               fetchrow=True)

    async def get_express_id_by_user_id(self, user_id: int):
        return await self.execute("SELECT * FROM express_id WHERE user_id=$1", user_id, fetchrow=True)

    async def add_user(self, user_id: int, lang: str = 'uz'):
        sql = """
        INSERT INTO Users(user_id, lang) VALUES($1, $2)
        """
        await self.execute(sql, user_id, lang, execute=True)

    async def get_user_lang(self, user_id):
        sql = "SELECT lang FROM users WHERE user_id=$1"
        res = await self.execute(sql, user_id, fetchrow=True)
        if res:
            return res[0]

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_lang(self, lang, user_id):
        sql = "UPDATE users SET lang=$1 WHERE user_id=$2"
        return await self.execute(sql, lang, user_id, execute=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    async def get_user_by_id(self, user_id: int):
        sql = "SELECT * FROM Users WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def add_express_id(self, user_id, express_id, full_name, phone_number, passport_seria,
                             passport_pnfl, birth_date, address, filial, passport_front, passport_back):
        sql = (
            "INSERT INTO express_id(user_id, express_id, full_name, phone_number, passport_seria, "
            "passport_pnfl, birth_date, address, filial, passport_front, passport_back) "
            "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) RETURNING id")
        result = await self.execute(sql, user_id, express_id, full_name, phone_number, passport_seria,
                                    passport_pnfl, birth_date, address, filial, passport_front, passport_back,
                                    fetch=True)
        return result[0]['id'] if result else None

    async def add_express_id2(self, user_id, express_id, full_name, phone_number, passport_seria,
                              passport_pnfl, address):
        sql = (
            "INSERT INTO express_id(user_id, express_id, full_name, phone_number, passport_seria, "
            "passport_pnfl,  address) "
            "VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING id")
        result = await self.execute(sql, user_id, express_id, full_name, phone_number, passport_seria,
                                    passport_pnfl, address,
                                    fetch=True)

        return result[0]['id'] if result else None

    async def update_express_id_status(self, id, status):
        sql = "UPDATE express_id SET status=$1 WHERE id=$2"
        return await self.execute(sql, status, id, execute=True)

    async def update_ref_user_id_status(self, id, status):
        sql = "UPDATE ref_users_id SET status=$1 WHERE id=$2"
        return await self.execute(sql, status, id, execute=True)

    async def get_all_uzb_delivered_products_payment(self, date):
        return await self.execute("""
SELECT 
    CAST(id AS VARCHAR) AS id, 
    user_id, 
    id_code, 
    kg, 
    date, 
    'achchot' AS kategoriya,
    CAST(REPLACE(CAST(price AS TEXT), '.', '') AS NUMERIC) AS amount, 
    created_at, 
    'product_payments' AS source
FROM uzb_delivered_products_payment
WHERE status = TRUE
AND TO_CHAR(created_at, 'MM.YYYY') = $1

UNION ALL

SELECT 
    CAST(id AS VARCHAR) AS id, 
    NULL AS user_id,          
    NULL AS id_code,          
    NULL AS kg,               
    NULL AS date,
    type AS kategoriya,            
    CAST(REPLACE(CAST(amount AS TEXT), '.', '') AS NUMERIC) AS amount, 
    created_at, 
    'expenses' AS source
FROM expenses
WHERE TO_CHAR(created_at, 'MM.YYYY') = $1

ORDER BY created_at DESC

        """, date, fetch=True)


    async def delete_express_id(self, data_id):
        sql = "DELETE FROM express_id WHERE id=$1"
        return await self.execute(sql, data_id, execute=True)

    async def delete_ref_user_id(self, data_id):
        sql = "DELETE FROM ref_users_id WHERE id=$1"
        return await self.execute(sql, data_id, execute=True)

    async def get_express_id_by_id(self, data_id):
        sql = "SELECT * FROM express_id WHERE id=$1"
        return await self.execute(sql, data_id, fetchrow=True)

    async def update_user(self,
                          user_id: int,
                          full_name: str,
                          phone_number: str,
                          passport_id: str,
                          region: str,
                          express_id: str = "", ):
        sql = """
        UPDATE users SET full_name=$1, phone_number=$2, passport_id=$3, region=$4, express_id=$6 WHERE user_id=$5
        """
        return await self.execute(sql, full_name, phone_number, passport_id, region, user_id, express_id,
                                  execute=True)

    async def select_last_added_express_id(self):
        return await self.execute("SELECT * FROM express_id ORDER BY created_at DESC", fetch=True)

    async def all_user_count(self):
        res = await self.execute("""SELECT COUNT(id) FROM users""", fetch=True)
        if res:
            return res[0]['count']
        else:
            return False

    async def count_today_added_users(self):
        res = await self.execute("""SELECT COUNT(id) FROM users WHERE DATE(created_at) = CURRENT_DATE;""", fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def count_week_added_users(self):
        res = await self.execute(
            """SELECT COUNT(id) FROM users WHERE created_at >= CURRENT_DATE - INTERVAL 
            '1 week' AND created_at < CURRENT_DATE + INTERVAL '1 day';""", fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def count_month_added_users(self):
        res = await self.execute(
            """SELECT COUNT(id) FROM users WHERE created_at >= CURRENT_DATE - INTERVAL 
            '1 month' AND created_at < CURRENT_DATE + INTERVAL '1 day';""", fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def last12hour_added_users(self):
        sql = """
        SELECT COUNT(id)
        FROM users
        WHERE created_at >= NOW() - INTERVAL '12 hours' AND created_at <= NOW();
        """
        res = await self.execute(sql, fetch=True)

        if res:
            return res[0]['count']
        else:
            return False

    async def all_express_id_count(self):
        res = await self.execute("""SELECT COUNT(id) FROM express_id""", fetch=True)
        if res:
            return res[0]['count']
        else:
            return False

    async def last12hour_added_express_id(self):
        sql = """
        SELECT COUNT(id)
        FROM express_id
        WHERE created_at >= NOW() - INTERVAL '12 hours' AND created_at <= NOW();
        """
        res = await self.execute(sql, fetch=True)

        if res:
            return res[0]['count']
        else:
            return False

    async def count_today_added_express_id(self):
        res = await self.execute("""SELECT COUNT(id) FROM express_id WHERE DATE(created_at) = CURRENT_DATE;""",
                                 fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def count_week_added_express_id(self):
        res = await self.execute(
            """SELECT COUNT(id) FROM express_id WHERE created_at >= CURRENT_DATE - INTERVAL 
            '1 week' AND created_at < CURRENT_DATE + INTERVAL '1 day';""", fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def count_month_added_express_id(self):
        res = await self.execute(
            """SELECT COUNT(id) FROM express_id WHERE created_at >= CURRENT_DATE - INTERVAL 
            '1 month' AND created_at < CURRENT_DATE + INTERVAL '1 day';""", fetch=True)
        if res:
            return res[0]['count']  # Accessing the count value from the first dictionary in the list
        else:
            return False

    async def compute_percent(self):
        sql = """
            SELECT
                COUNT(id) AS jami,
                SUM(CASE WHEN lang = 'en' THEN 1 ELSE 0 END) AS en_foiz,
                SUM(CASE WHEN lang = 'uz' THEN 1 ELSE 0 END) AS uz_foiz,
                SUM(CASE WHEN lang = 'ru' THEN 1 ELSE 0 END) AS ru_foiz,
                SUM(CASE WHEN lang = 'cn' THEN 1 ELSE 0 END) AS cn_foiz
            FROM users;
        """
        res = await self.execute(sql, fetch=True)
        # print(res)
        if res:
            result_str = ""
            for row in res:  # Iterate over the list of dictionaries
                result_str += (f"<i>🇺🇿 Uzbek foydalanuvchilar:</i> <b>{int(row['uz_foiz'])}</b> ta\n"
                               f"<i>🇷🇺 Rus foydalanuvchilar:</i> <b>{int(row['ru_foiz'])}</b> ta\n")
            return result_str
        else:
            return False

    async def get_all_express_id(self):
        return await self.execute("SELECT * FROM express_id", fetch=True)

    async def get_user_id_by_express_id(self, express_id):
        return await self.execute("SELECT * FROM express_id WHERE express_id LIKE '%' || $1 || '%'", express_id,
                                  fetchrow=True)

    async def get_user_id_by_express_id_equal(self, express_id):
        return await self.execute("SELECT * FROM express_id WHERE express_id=$1", express_id,
                                  fetchrow=True)

    async def get_price(self, type):
        return await self.execute("SELECT * FROM prices WHERE type=$1", type, fetchrow=True)


    async def check_track_code_base(self, track_code: str):
        return await self.execute("SELECT * FROM track_codes_base WHERE track_code=$1", track_code, fetch=True)


    async def insert_track_codes(self, track_code: str, weight=None, receive_date=None,
                                 product_name=None, count=0, reys_name=None):
        sql = (
            "INSERT INTO track_codes(track_code, weight, receive_date, product_name, count, reys_name) "
            "VALUES($1, $2, $3, $4, $5, $6)"
        )
        return await self.execute(sql, track_code, weight, receive_date, product_name, count, reys_name, execute=True)

    async def insert_track_codes_base(self, track_code: str, weight=None, receive_date=None,
                                 product_name=None, count=0, reys_name=None):
        sql = (
            "INSERT INTO track_codes_base(track_code, weight, receive_date, product_name, count, reys_name) "
            "VALUES($1, $2, $3, $4, $5, $6)"
        )
        return await self.execute(sql, track_code, weight, receive_date, product_name, count, reys_name, execute=True)

    async def update_track_status_china_receive(self, track_code):
        sql = "UPDATE track_codes SET receive_china=$1 WHERE track_code=$2"
        return await self.execute(sql, True, track_code, execute=True)

    async def update_track_status_receive_uz(self, track_code):
        sql = "UPDATE track_codes SET receive_uz=$1 WHERE track_code=$2"
        return await self.execute(sql, True, track_code, execute=True)

    async def check_uzb_track_code(self, track_code: str):
        return await self.execute("SELECT * FROM track_codes WHERE track_code=$1", track_code,
                                  fetchrow=True)

    async def get_track_code_data_by_track_code(self, track_code: str):
        return await self.execute("SELECT * FROM track_codes WHERE track_code=$1", track_code, fetchrow=True)

    async def get_track_code_data_by_track_code_base(self, track_code: str):
        return await self.execute("SELECT * FROM track_codes_base WHERE track_code LIKE '%' || $1 || '%'", track_code, fetchrow=True)

    async def add_uzb_delivered_payment(self,
                                        user_id: int,
                                        id_code: str,
                                        kg: str,
                                        date: str,
                                        product_count: str,
                                        price: str,
                                        photo_link: str,
                                        payment_pic_id: str = None,
                                        status: bool = False,
                                        type_product: str = 'ODDIY',
                                        flight_name: str = 'TOPCARGO',
                                        ):
        sql = ("""
        INSERT INTO uzb_delivered_products_payment
        (user_id, id_code, kg, date, product_count, price, payment_pic_id, status, photo_link, type_product, flight_name)
        VALUES 
        ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        RETURNING id
        """)
        result = await self.execute(sql, user_id, id_code, kg, date, product_count, price, payment_pic_id,
                                    status, photo_link, type_product, flight_name,
                                    fetch=True)
        print("RESULT ", result)
        return result[0]['id'] if result else None

    async def update_uzb_delivered_payment_status(self, id: int, status: bool = True):
        sql = "UPDATE uzb_delivered_products_payment SET status=$1 WHERE id=$2"
        return await self.execute(sql, status, id, execute=True)

    async def update_uzb_delivered_payment_pic_id(self, id: int, pic_id: str):
        sql = "UPDATE uzb_delivered_products_payment SET payment_pic_id=$1 WHERE id=$2"
        return await self.execute(sql, pic_id, id, execute=True)

    async def get_uzb_delivered_payment_data_by_id(self, id: int):
        return await self.execute("SELECT * FROM uzb_delivered_products_payment WHERE id=$1", id, fetchrow=True)

    async def get_uzb_delivered_payment_data_by_user_id(self, user_id: int):
        return await self.execute("SELECT * FROM uzb_delivered_products_payment WHERE user_id=$1", user_id,
                                  fetchrow=True)

    async def get_uzb_delivered_payment_data_by_id_code(self, id_code: str):
        return await self.execute("SELECT * FROM uzb_delivered_products_payment WHERE id_code=$1", id_code,
                                  fetchrow=True)

    async def get_data_by_id_uzb_delivered_products_payment(self, id):
        return await self.execute("SELECT * FROM uzb_delivered_products_payment WHERE id=$1", id, fetchrow=True)

    async def check_delivery_data_product_by_user_id(self, user_id):
        return await self.execute("SELECT * FROM delivered_products WHERE user_id=$1", user_id, fetchrow=True)

    async def update_name_delivery_data_product_by_user_id(self, user_id, name):
        sql = "UPDATE delivered_products SET name=$1 WHERE user_id=$2"
        return await self.execute(sql, name, user_id, execute=True)

    async def update_phone_number_delivery_data_product_by_user_id(self, user_id, phone_number):
        sql = "UPDATE delivered_products SET phone_number=$1 WHERE user_id=$2"
        return await self.execute(sql, phone_number, user_id, execute=True)

    async def update_address_delivery_data_product_by_user_id(self, user_id, address):
        sql = "UPDATE delivered_products SET address=$1 WHERE user_id=$2"
        return await self.execute(sql, address, user_id, execute=True)

    async def update_mail_type_delivery_data_products_by_user_id(self, user_id, mail_type):
        sql = "UPDATE delivered_products SET mail_type=$1 WHERE user_id=$2"
        return await self.execute(sql, mail_type, user_id, execute=True)

    async def insert_delivery_products(self, user_id, name, phone_number, uzb_id, address, mail_type):
        sql = "INSERT INTO delivered_products(user_id, name, phone_number, uzb_id, address, mail_type) VALUES($1, $2, $3, $4, $5, $6)"
        return await self.execute(sql, user_id, name, phone_number, uzb_id, address, mail_type, execute=True)

    async def create_ref_link(self, user_id, name, link_code, express_code, price, link):
        sql = "INSERT INTO teachers(user_id, name, link_code, express_code, price, link) VALUES($1, $2, $3, $4, $5, $6)"
        return await self.execute(sql, user_id, name, link_code, express_code, price, link, execute=True)

    async def get_ref_link_by_user_id(self, user_id):
        return await self.execute("SELECT * FROM teachers WHERE user_id=$1", user_id, fetchrow=True)

    async def get_ref_link_by_link_code(self, link_code):
        return await self.execute("SELECT * FROM teachers WHERE link_code=$1", link_code, fetchrow=True)

    async def get_ref_link_by_express_code(self, express_code):
        return await self.execute("SELECT * FROM teachers WHERE express_code=$1", express_code, fetchrow=True)

    async def get_ref_link_by_link(self, link):
        return await self.execute("SELECT * FROM teachers WHERE link=$1", link, fetchrow=True)

    async def update_ref_link_balance(self, user_id, balance):
        sql = "UPDATE teachers SET balance=$1 WHERE user_id=$2"
        return await self.execute(sql, balance, user_id, execute=True)

    async def get_all_ref_links(self):
        return await self.execute("SELECT * FROM teachers", fetch=True)

    async def get_all_ref_links_count(self):
        res = await self.execute("""SELECT COUNT(id) FROM teachers""", fetch=True)
        if res:
            return res[0]['count']
        else:
            return False

    async def get_all_ref_links_balance(self):
        res = await self.execute("""SELECT SUM(balance) FROM teachers""", fetch=True)
        if res:
            return res[0]['sum']
        else:
            return False

    async def update_ref_link_balance_by_link_code(self, link_code, balance):
        sql = "UPDATE teachers SET balance=$1 WHERE link_code=$2"
        return await self.execute(sql, balance, link_code, execute=True)

    async def update_ref_link_balance_by_express_code(self, express_code, balance):
        sql = "UPDATE teachers SET balance=$1 WHERE express_code=$2"
        return await self.execute(sql, balance, express_code, execute=True)

    async def update_ref_link_price(self, user_id, price):
        sql = "UPDATE teachers SET price=$1 WHERE user_id=$2"
        return await self.execute(sql, price, user_id, execute=True)

    async def update_card_data(self, user_id, card_number, card_name):
        sql = "UPDATE teachers SET card_name=$1, card_number=$3 WHERE user_id=$2"
        return await self.execute(sql, card_name, user_id, card_number, execute=True)

    async def add_transaction(self, teacher_id, amount, status):
        sql = "INSERT INTO teacher_transactions(teacher_id, amount, status) VALUES($1, $2, $3)"
        return await self.execute(sql, teacher_id, amount, status, execute=True)

    async def update_transaction_status(self, teacher_id, status):
        sql = "UPDATE teacher_transactions SET status=$1 WHERE teacher_id=$2 AND status='pending'"
        return await self.execute(sql, status, teacher_id, execute=True)

    async def get_transaction_by_id(self, id):
        return await self.execute("SELECT * FROM teacher_transactions WHERE id=$1", id, fetchrow=True)

    async def get_all_transactions(self):
        return await self.execute("SELECT * FROM teacher_transactions", fetch=True)

    async def get_all_transactions_count(self):
        res = await self.execute("""SELECT COUNT(id) FROM teacher_transactions""", fetch=True)
        if res:
            return res[0]['count']
        else:
            return False

    async def get_all_transactions_amount(self):
        res = await self.execute("""SELECT SUM(amount) FROM teacher_transactions""", fetch=True)
        if res:
            return res[0]['sum']
        else:
            return False

    async def get_all_transactions_amount_by_status(self, status):
        res = await self.execute("""SELECT SUM(amount) FROM teacher_transactions WHERE status=$1""", status, fetch=True)
        if res:
            return res[0]['sum']
        else:
            return False

    async def get_transaction_by_teacher_id(self, teacher_id):
        return await self.execute("SELECT COUNT(*) FROM teacher_transactions WHERE teacher_id=$1 AND  status='success'",
                                  teacher_id, fetch=True)

    async def get_amount_by_teacher_id(self, teacher_id):
        res = await self.execute("""SELECT SUM(CAST(amount AS NUMERIC)) 
FROM teacher_transactions 
WHERE teacher_id=$1 AND status='success';""", teacher_id,
                                 fetch=True)
        if res:
            return res[0]['sum']
        else:
            return False

    async def update_transaction_photo_id(self, teacher_id, photo_id):
        sql = "UPDATE teacher_transactions SET photo=$1 WHERE teacher_id=$2 AND status='pending'"
        return await self.execute(sql, photo_id, teacher_id, execute=True)

    async def get_transaction_by_teacher_id_status_pending(self, teacher_id):
        return await self.execute("SELECT * FROM teacher_transactions WHERE teacher_id=$1 AND status='pending'",
                                  teacher_id, fetch=True)

    async def add_referral_user(self, user_id, teacher_id, name, express_code, link_code):
        sql = "INSERT INTO referral_users(user_id, teacher_id, name, express_code, link_code) VALUES($1, $2, $3, $4, $5)"
        return await self.execute(sql, user_id, teacher_id, name, express_code, link_code, execute=True)

    async def get_referral_user_by_user_id(self, user_id):
        return await self.execute("SELECT * FROM referral_users WHERE user_id=$1", user_id, fetchrow=True)

    async def get_referral_user_by_teacher_id(self, teacher_id):
        return await self.execute("SELECT COUNT(*) FROM referral_users WHERE teacher_id=$1", teacher_id, fetch=True)

    async def get_referral_user_by_link_code(self, link_code):
        return await self.execute("SELECT * FROM referral_users WHERE link_code=$1", link_code, fetch=True)

    async def get_referral_user_by_express_code(self, express_code):
        return await self.execute("SELECT * FROM referral_users WHERE express_code=$1", express_code, fetch=True)

    async def add_ref_users_id(self, user_id, teacher_id, express_id,
                               full_name, phone_number, passport_seria,
                               passport_pnfl, birth_date, address, filial,
                               passport_front, passport_back):
        sql = ("INSERT INTO ref_users_id(user_id, teacher_id, express_id, "
               "full_name, phone_number, passport_seria, passport_pnfl, "
               "birth_date, address, filial, passport_front, passport_back) VALUES($1, $2, $3, $4, $5, $6, $7, "
               "$8, $9, $10, $11, $12) RETURNING id")
        result = await self.execute(sql, user_id, teacher_id, express_id, full_name,
                                    phone_number, passport_seria, passport_pnfl, birth_date,
                                    address, filial, passport_front, passport_back, fetch=True)

        return result[0]['id'] if result else None

    async def get_ref_users_id_by_user_id(self, user_id):
        return await self.execute("SELECT * FROM ref_users_id WHERE user_id=$1", user_id, fetchrow=True)

    async def get_ref_users_id_by_id(self, id):
        return await self.execute("SELECT * FROM ref_users_id WHERE id=$1", id, fetchrow=True)

    async def get_ref_users_id_by_teacher_id(self, teacher_id):
        return await self.execute("""SELECT COUNT(*)
FROM ref_users_id
WHERE teacher_id = $1;""", teacher_id, fetch=True)

    async def get_ref_users_id_by_express_id(self, express_id):
        return await self.execute("SELECT * FROM ref_users_id WHERE express_id=$1", express_id, fetch=True)

    async def select_last_added_ref_users_id(self):
        return await self.execute("SELECT * FROM ref_users_id ORDER BY created_at DESC", fetch=True)

    async def get_user_id_by_ref_users_id(self, express_id):
        return await self.execute("SELECT * FROM ref_users_id WHERE express_id LIKE '%' || $1 || '%'", express_id,
                                  fetchrow=True)

    async def get_teacher_data_by_express_code(self, express_code):
        return await self.execute("SELECT * FROM teachers WHERE express_code LIKE '%' || $1 || '%'", express_code,
                                  fetchrow=True)

    async def add_expense(self, amount, type):
        sql = "INSERT INTO expenses(amount, type) VALUES($1, $2)"
        return await self.execute(sql, amount, type, execute=True)

    async def select_all_expenses(self):
        return await self.execute("SELECT * FROM expenses", fetch=True)

    async def select_expense_by_type(self, type):
        return await self.execute("SELECT * FROM expenses WHERE type=$1", type, fetch=True)

    async def select_expense_by_id(self, id):
        return await self.execute("SELECT * FROM expenses WHERE id=$1", id, fetchrow=True)

    async def select_expense_by_amount(self, amount):
        return await self.execute("SELECT * FROM expenses WHERE amount=$1", amount, fetch=True)

    async def get_all_users_not_payed(self):
        return await self.execute("""
            SELECT *
            FROM uzb_delivered_products_payment
            WHERE status = FALSE
              AND created_at <= NOW() - INTERVAL '48 hours';
                    """, fetch=True)

    async def check_user_flight_is_vip(self, user_id):
        sql = """
        WITH last_flights AS (
            SELECT flight_name, MAX(created_at) AS created_at
            FROM uzb_delivered_products_payment
            WHERE user_id = $1
            GROUP BY flight_name
            ORDER BY created_at DESC
            LIMIT 3
        ),
        flight_kg AS (
            SELECT d.flight_name, SUM(CAST(d.kg AS FLOAT)) AS total_kg
            FROM last_flights lf
            JOIN uzb_delivered_products_payment d
              ON d.flight_name = lf.flight_name AND d.user_id = $1
            GROUP BY d.flight_name
            ORDER BY MAX(d.created_at) DESC
        )
        SELECT total_kg FROM flight_kg;
        """
        return await self.execute(sql, user_id, fetch=True)

    async def update_express_id_is_vip_by_user_id(self, user_id, is_vip):
        sql = "UPDATE express_id SET is_vip=$1 WHERE user_id=$2"
        return await self.execute(sql, is_vip, user_id, execute=True)
#     async def get_last_complaints_sum(self):
#         sql = """
#         SELECT
#     SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
# FROM
#     uzb_delivered_products_payment
# WHERE
#     created_at >= CURRENT_DATE - INTERVAL '1 day'
#     AND created_at < CURRENT_DATE + INTERVAL '1 day';
#         """
#         return await self.execute(sql, fetch=True)


    async def get_last_complaints_sum(self):
        sql = """
        WITH categorized_data AS (
    SELECT
        CASE
            WHEN id_code LIKE 'TCH%' THEN 'Chilonzor'
            WHEN id_code LIKE 'TPP%' THEN 'Parkent'
            ELSE 'Boshqa'
            END AS location,
        type_product,
        ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
        SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
    FROM uzb_delivered_products_payment
    WHERE created_at >= CURRENT_DATE - INTERVAL '2 day'
      AND created_at < CURRENT_DATE + INTERVAL '2 day'
    GROUP BY location, type_product
),
     total_data AS (
         SELECT
             CASE
                 WHEN id_code LIKE 'TCH%' THEN 'Chilonzor'
                 WHEN id_code LIKE 'TPP%' THEN 'Parkent'
                 ELSE 'Boshqa'
                 END AS location,
             'TOTAL' AS type_product,
             ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
             SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
         FROM uzb_delivered_products_payment
         WHERE created_at >= CURRENT_DATE - INTERVAL '2 day'
           AND created_at < CURRENT_DATE + INTERVAL '2 day'
         GROUP BY location

         UNION ALL

         SELECT
             CASE
                 WHEN id_code LIKE 'TCH%' THEN 'Chilonzor'
                 WHEN id_code LIKE 'TPP%' THEN 'Parkent'
                 ELSE 'Boshqa'
                 END AS location,
             'TOTAL_PAID' AS type_product,
             ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
             SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
         FROM uzb_delivered_products_payment
         WHERE created_at >= CURRENT_DATE - INTERVAL '2 day'
           AND created_at < CURRENT_DATE + INTERVAL '2 day'
           AND status = true
         GROUP BY location

         UNION ALL

         SELECT
             CASE
                 WHEN id_code LIKE 'TCH%' THEN 'Chilonzor'
                 WHEN id_code LIKE 'TPP%' THEN 'Parkent'
                 ELSE 'Boshqa'
                 END AS location,
             'TOTAL_NOTPAID' AS type_product,
             ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
             SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
         FROM uzb_delivered_products_payment
         WHERE created_at >= CURRENT_DATE - INTERVAL '2 day'
           AND created_at < CURRENT_DATE + INTERVAL '2 day'
           AND status = false
         GROUP BY location
     ),
     final_data AS (
         SELECT * FROM categorized_data
         UNION ALL
         SELECT * FROM total_data
     ),
     overall_total AS (
         SELECT
             'Jami' AS location,
             type_product,
             ROUND(SUM(total_weight), 1) AS total_weight,
             SUM(total_sum) AS total_sum
         FROM final_data
         GROUP BY type_product
     )
SELECT *
FROM (
         SELECT * FROM final_data
         UNION ALL
         SELECT * FROM overall_total
     ) AS sorted_data
ORDER BY
    CASE location
        WHEN 'Chilonzor' THEN 1
        WHEN 'Parkent' THEN 2
        WHEN 'Boshqa' THEN 3
        WHEN 'Jami' THEN 4
        ELSE 5
        END,
    type_product;
"""
        return await self.execute(sql, fetch=True)

    async def get_all_cards(self):
        return await self.execute("SELECT * FROM cards", fetch=True)

    async def get_card_by_id(self, id):
        return await self.execute("SELECT * FROM cards WHERE id=$1", id, fetchrow=True)

    async def update_card_by_id(self, id, card_number, card_name):
        sql = "UPDATE cards SET card_number=$1, card_name=$3 WHERE id=$2"
        return await self.execute(sql, card_number, id, card_name, execute=True)

    async def delete_card_by_id(self, id):
        return await self.execute("DELETE FROM cards WHERE id=$1", id, execute=True)

    async def insert_card(self, card_number, card_name, branch_code):
        sql = "INSERT INTO cards(card_number, card_name, branch_code) VALUES($1, $2, $3)"
        return await self.execute(sql, card_number, card_name, branch_code, execute=True)



    async def get_id_by_code(self, code):
        return await self.execute("""
        SELECT express_id 
        FROM express_id 
        WHERE express_id LIKE $1 || '-%' 
        ORDER BY CAST(SPLIT_PART(express_id, '-', 2) AS INTEGER) DESC 
        LIMIT 1;

        """, code, fetch=True)

    async def get_branch_channel_by_branch_code(self, branch_code):
        return await self.execute("SELECT * FROM branch_info WHERE branch_code=$1", branch_code, fetchrow=True)

    async def get_branch_data_by_admin_id(self, admin_id):
        return await self.execute("SELECT * FROM branch_info WHERE admin_id=$1", admin_id, fetchrow=True)

    async def get_all_cards_by_branch_code(self, branch_code):
        return await self.execute("SELECT * FROM cards WHERE branch_code=$1", branch_code, fetch=True)

    async def count_express_id_by_prefix(self, prefix: str):
        queries = {
            "today": f"SELECT COUNT(id) FROM express_id WHERE DATE(created_at) = CURRENT_DATE AND express_id LIKE '{prefix}%'",
            "week": f"SELECT COUNT(id) FROM express_id WHERE created_at >= CURRENT_DATE - INTERVAL '1 week' AND created_at < CURRENT_DATE + INTERVAL '1 day' AND express_id LIKE '{prefix}%'",
            "month": f"SELECT COUNT(id) FROM express_id WHERE created_at >= CURRENT_DATE - INTERVAL '1 month' AND created_at < CURRENT_DATE + INTERVAL '1 day' AND express_id LIKE '{prefix}%'",
            "last12hours": f"SELECT COUNT(id) FROM express_id WHERE created_at >= NOW() - INTERVAL '12 hours' AND created_at <= NOW() AND express_id LIKE '{prefix}%'",
        }
        results = {}
        for key, query in queries.items():
            res = await self.execute(query, fetch=True)
            results[key] = res[0]['count'] if res else 0

        return results