CREATE TABLE IF NOT EXISTS users
(
    id         SERIAL PRIMARY KEY,
    user_id    BIGINT UNIQUE NOT NULL,
    lang       VARCHAR(8)    NOT NULL,
    created_at TIMESTAMP default CURRENT_TIMESTAMP
);



DROP TABLE users;


CREATE TYPE express_id_status AS ENUM ('accepted', 'rejected', 'pending');
CREATE TABLE IF NOT EXISTS express_id
(
    id             SERIAL PRIMARY KEY,
    user_id        BIGINT      NOT NULL,
    express_id     VARCHAR(64) NOT NULL,
    full_name      VARCHAR(128)      default NULL,
    phone_number   VARCHAR(128)      default NULL,
    passport_seria VARCHAR(128)      default NULL,
    passport_pnfl  VARCHAR(128)      default NULL,
    birth_date     VARCHAR(128)      default NULL,
    address        VARCHAR(128)      default NULL,
    filial         VARCHAR(128)      default NULL,
    passport_front VARCHAR(128)      default NULL,
    passport_back  VARCHAR(128)      default NULL,
    status         express_id_status DEFAULT 'pending',
    created_at     TIMESTAMP         default CURRENT_TIMESTAMP
);

DROP TABLE express_id;

--
--
-- SELECT SUM(CASE WHEN created_at >= NOW() - INTERVAL '12 hours' THEN 1 ELSE 0 END) AS last_12_hours,
--        SUM(CASE WHEN DATE(created_at) = CURRENT_DATE THEN 1 ELSE 0 END)           AS today,
--        SUM(CASE
--                WHEN created_at >= CURRENT_DATE - INTERVAL '1 week' AND created_at < CURRENT_DATE + INTERVAL '1 day'
--                    THEN 1
--                ELSE 0 END)                                                        AS last_week,
--        SUM(CASE
--                WHEN created_at >= CURRENT_DATE - INTERVAL '1 month' AND created_at < CURRENT_DATE + INTERVAL '1 day'
--                    THEN 1
--                ELSE 0 END)                                                        AS last_month
-- FROM users;
--
--
--
-- SELECT COUNT(id)                                                        AS jami,
--        SUM(CASE WHEN lang = 'en' THEN 1 ELSE 0 END)                     AS en_soni,
--        SUM(CASE WHEN lang = 'uz' THEN 1 ELSE 0 END)                     AS uz_soni,
--        SUM(CASE WHEN lang = 'ru' THEN 1 ELSE 0 END)                     AS ru_soni,
--        SUM(CASE WHEN lang = 'cn' THEN 1 ELSE 0 END)                     AS cn_soni,
--        (SUM(CASE WHEN lang = 'en' THEN 1 ELSE 0 END) / COUNT(id)) * 100 AS en_foiz_percent,
--        (SUM(CASE WHEN lang = 'uz' THEN 1 ELSE 0 END) / COUNT(id)) * 100 AS uz_foiz_percent,
--        (SUM(CASE WHEN lang = 'ru' THEN 1 ELSE 0 END) / COUNT(id)) * 100 AS ru_foiz_percent,
--        (SUM(CASE WHEN lang = 'cn' THEN 1 ELSE 0 END) / COUNT(id)) * 100 AS cn_foiz_percent
-- FROM users;


CREATE TABLE IF NOT EXISTS track_codes
(
    id            SERIAL PRIMARY KEY,
    track_code    VARCHAR(128) NOT NULL,
    weight        FLOAT                 DEFAULT NULL,
    receive_china BOOLEAN               DEFAULT FALSE,
    out_china     BOOLEAN               DEFAULT FALSE,
    receive_uz    BOOLEAN               DEFAULT FALSE,
    created_at    TIMESTAMP             default CURRENT_TIMESTAMP,
    photo_link    TEXT         NOT NULL DEFAULT 'https://telegra.ph/file/955f8d30cdc3961bce5ab.png'
);

-- DROP TABLE track_codes;

CREATE TABLE prices
(
    id         SERIAL PRIMARY KEY,
    type       VARCHAR(128) NOT NULL,
    price      VARCHAR(128) NOT NULL,
    created_at TIMESTAMP default CURRENT_TIMESTAMP
);

INSERT INTO prices (type, price)
VALUES ('auto_express', '7.9');
INSERT INTO prices (type, price)
VALUES ('avia_express', '9.5');
INSERT INTO prices (type, price)
VALUES ('cargo', '5.5');


CREATE TABLE IF NOT EXISTS delivered_products
(
    id           SERIAL PRIMARY KEY,
    user_id      BIGINT       NOT NULL,
    name         VARCHAR(128) NOT NULL,
    phone_number VARCHAR(256) NOT NULL,
    uzb_id       VARCHAR(256) NOT NULL,
    address      VARCHAR(256) NOT NULL,
    mail_type    VARCHAR(256) NOT NULL,
    created_at   TIMESTAMP default CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL
);

DROP TABLE delivered_products;

CREATE TABLE IF NOT EXISTS track_codes
(
    id            SERIAL PRIMARY KEY,
    track_code    VARCHAR(128) NOT NULL,
    weight        FLOAT        DEFAULT NULL,
    receive_date   VARCHAR      DEFAULT NULL,
    product_name  VARCHAR      DEFAULT NULL,
    count        INTEGER      DEFAULT 0,
    reys_name     VARCHAR      DEFAULT NULL,
    created_at    TIMESTAMP    default CURRENT_TIMESTAMP
);
drop TABLE track_codes;


-- CREATE TABLE prices
-- (
--     id         SERIAL PRIMARY KEY,
--     type       VARCHAR(128) NOT NULL,
--     price      VARCHAR(128) NOT NULL,
--     created_at TIMESTAMP default CURRENT_TIMESTAMP
-- );


DROP TABLE uzb_delivered_products_payment;
DROP TABLE delivered_products;



CREATE TABLE IF NOT EXISTS uzb_delivered_products_payment
(
    id             SERIAL PRIMARY KEY,
    user_id        BIGINT       NOT NULL,
    id_code        VARCHAR(128) NOT NULL,
    kg             VARCHAR(256) NOT NULL,
    date           VARCHAR(256) NOT NULL,
    product_count  VARCHAR(256) NOT NULL,
    price          VARCHAR(256) NOT NULL,
    payment_pic_id VARCHAR(256) DEFAULT NULL,
    status         BOOLEAN      default False,
    photo_link     TEXT         DEFAULT 'https://i.postimg.cc/DwhG8GQF/photo-2024-08-17-16-28-11.jpg',
    created_at     TIMESTAMP    default CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL
);

DROP TABLE uzb_delivered_products_payment;


CREATE TABLE IF NOT EXISTS teachers
(
    id           SERIAL PRIMARY KEY,
    user_id      BIGINT       NOT NULL,
    name         VARCHAR(128) NOT NULL,
    link_code    VARCHAR(128) NOT NULL,
    express_code VARCHAR(128) NOT NULL,
    price        VARCHAR(128) NOT NULL,
    link         VARCHAR(128) NOT NULL,
    balance      VARCHAR(128) DEFAULT '0',
    card_number  VARCHAR(128) DEFAULT NULL,
    card_name    VARCHAR(128) DEFAULT NULL,
    created_at   TIMESTAMP    default CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL
);

DROP TABLE teachers;

CREATE TYPE teacher_status AS ENUM ('success', 'rejected', 'pending');
CREATE TABLE IF NOT EXISTS teacher_transactions
(
    id         SERIAL PRIMARY KEY,
    teacher_id BIGINT       NOT NULL,
    amount     VARCHAR(128) NOT NULL,
    photo      TEXT           DEFAULT NULL,
    status     teacher_status DEFAULT 'pending',
    created_at TIMESTAMP      default CURRENT_TIMESTAMP
);

DROP TABLE teacher_transactions;


CREATE TABLE IF NOT EXISTS referral_users
(
    id           SERIAL PRIMARY KEY,
    user_id      BIGINT       NOT NULL,
    teacher_id   BIGINT       NOT NULL,
    name         VARCHAR(128) NOT NULL,
    express_code VARCHAR(125) NOT NULL,
    link_code    VARCHAR(125) NOT NULL,
    created_at   TIMESTAMP default CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL,
    CONSTRAINT fk_teacher_id
        FOREIGN KEY (teacher_id)
            REFERENCES teachers (user_id)
            ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ref_users_id
(
    id             SERIAL PRIMARY KEY,
    user_id        BIGINT      NOT NULL,
    teacher_id     BIGINT      NOT NULL,
    express_id     VARCHAR(64) NOT NULL,
    full_name      VARCHAR(128)      default NULL,
    phone_number   VARCHAR(128)      default NULL,
    passport_seria VARCHAR(128)      default NULL,
    passport_pnfl  VARCHAR(128)      default NULL,
    birth_date     VARCHAR(128)      default NULL,
    address        VARCHAR(128)      default NULL,
    filial         VARCHAR(128)      default NULL,
    passport_front VARCHAR(128)      default NULL,
    passport_back  VARCHAR(128)      default NULL,
    status         express_id_status DEFAULT 'pending',
    created_at     TIMESTAMP         default CURRENT_TIMESTAMP,
    CONSTRAINT fk_ref_user_id
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
            ON DELETE SET NULL,
    CONSTRAINT fk_ref_teacher_id
        FOREIGN KEY (teacher_id)
            REFERENCES teachers (user_id)
            ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS expenses(
    id SERIAL PRIMARY KEY,
    amount BIGINT NOT NULL DEFAULT 0,
    type VARCHAR(60) NOT NULL DEFAULT 'xarajat',
    created_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS income(
    id SERIAL PRIMARY KEY,
    amount BIGINT NOT NULL DEFAULT 0,
    type VARCHAR(60) NOT NULL DEFAULT 'daromad',
    created_at TIMESTAMP DEFAULT current_timestamp
);


CREATE TYPE type_product_enum AS ENUM ('ODDIY', 'GABARIT', 'SERIYA', 'BREND');
ALTER TABLE uzb_delivered_products_payment
ADD COLUMN type_product type_product_enum DEFAULT 'ODDIY';


ALTER TABLE uzb_delivered_products_payment
ALTER COLUMN type_product TYPE TEXT;

SELECT
    type_product,
    SUM(CAST(kg AS FLOAT)) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '1 day'
    AND created_at < CURRENT_DATE + INTERVAL '1 day'
GROUP BY
    type_product

UNION ALL

SELECT
    'TOTAL' AS type_product,
    SUM(CAST(kg AS FLOAT)) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '1 day'
    AND created_at < CURRENT_DATE + INTERVAL '1 day';


















SELECT
    type_product,
    ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '1 day'
    AND created_at < CURRENT_DATE + INTERVAL '1 day'
GROUP BY
    type_product

UNION ALL

SELECT
    'TOTAL' AS type_product,
    ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '2 day'
    AND created_at < CURRENT_DATE + INTERVAL '2 day'

UNION ALL

SELECT
    'TOTAL_PAID' AS type_product,
    ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '2 day'
    AND created_at < CURRENT_DATE + INTERVAL '2 day'
    AND status = true

UNION ALL

SELECT
    'TOTAL_NOTPAID' AS type_product,
    ROUND(SUM(CAST(kg AS NUMERIC)), 1) AS total_weight,
    SUM(CAST(REPLACE(price, '.', '') AS BIGINT)) AS total_sum
FROM
    uzb_delivered_products_payment
WHERE
    created_at >= CURRENT_DATE - INTERVAL '2 day'
    AND created_at < CURRENT_DATE + INTERVAL '2 day'
    AND status = false;






CREATE TABLE IF NOT EXISTS cards
(
    id         SERIAL PRIMARY KEY,
    card_number VARCHAR(128) NOT NULL,
    card_name   VARCHAR(128) NOT NULL,
    branch_code VARCHAR(3) DEFAULT NULL,
    created_at TIMESTAMP    default CURRENT_TIMESTAMP
);

INSERT INTO cards (card_number, card_name, branch_code)
VALUES ('5614 6835 1745 1795', 'AZMIDINOV JAVOHIR', 'TPP');


CREATE TABLE IF NOT EXISTS branch_info
(
    id         SERIAL PRIMARY KEY,
    branch_code  VARCHAR(3)       NOT NULL,
    admin_username VARCHAR(128) NOT NULL,
    admin_id BIGINT NOT NULL,
    channel_id VARCHAR(128) NOT NULL,
    complaint_channel_id VARCHAR(128) DEFAULT NULL,
    pickup_channel VARCHAR(128) DEFAULT NULL,
    payment_channel VARCHAR(128) DEFAULT NULL,
    delivery_channel_id VARCHAR(128) DEFAULT NULL,
    delivered_channel VARCHAR(128) DEFAULT NULL,
    parent_branch_id INTEGER DEFAULT NULL,
    created_at TIMESTAMP    default CURRENT_TIMESTAMP,
    CONSTRAINT fk_parent_branch_id
        FOREIGN KEY (parent_branch_id)
            REFERENCES branch_info (id)
            ON DELETE SET NULL
);

ALTER TABLE branch_info
ADD COLUMN pickup_channel VARCHAR(128) DEFAULT NULL;
ALTER TABLE branch_info
ADD COLUMN payment_channel VARCHAR(128) DEFAULT NULL;
ALTER TABLE branch_info
ADD COLUMN delivered_channel VARCHAR(128) DEFAULT NULL;

SELECT * FROM branch_info WHERE branch_code = 'TCH';


INSERT INTO branch_info (
                         branch_code,
                         admin_username,
                         admin_id,
                         channel_id,
                         complaint_channel_id
) VALUES (
          'TPP',
          '@topcargo_admin',
          '7690861611',
          '-1002292852144',
          '-1002383624937'
         );





CREATE TABLE track_codes_base (
    id SERIAL PRIMARY KEY ,
    track_code character varying(128) NOT NULL,
    "weight" double precision,
    "receive_date" character varying,
    "product_name" character varying,
    "count" integer DEFAULT '0',
    "reys_name" character varying,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP
);
