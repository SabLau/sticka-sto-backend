import datetime
import os
import sys
import random
import string
import psycopg2

from random import randint



# os.environ.get returns None if the variable doesn't exist
database = os.environ.get('STICKA_STO_DB_NAME')
host = os.environ.get('STICKA_STO_DB_HOST')
port = os.environ.get('STICKA_STO_DB_PORT')
password = os.environ.get('STICKA_STO_AD_PW')
user = os.environ.get('STICKA_STO_USER')

# throw error if the variables do not exist in the environment variables
if not (database and host and port and password and user):
    sys.exit("""You have not set all environment variables. Check for:
        * STICKA_STO_DB_NAME
        * STICKA_STO_DB_HOST
        * STICKA_STO_DB_PORT
        * STICKA_STO_AD_PW
        * STICKA_STO_USER """
    )

#set environment variables for db info
conn = psycopg2.connect(
    database=database,
    host=host,
    port=port,
    password = password,
    user = user
)

#connects to db allowing you to access db
cur = conn.cursor()

#Initialize all variables for Queries
customer_name_1 = "dummy"
customer_email_1 = "dummy@email.com"

customer_name_2 = "dumberlina"
customer_email_2 = "dumberlina@email.com"

customer_name_3 = "dumbotron"
customer_email_3 = "dumbotron@email.com"

customer_name_4 = "majong"
customer_email_4 = "majong@email.com"

customer_name_5 = "longman"
customer_email_5 = "longman@email.com"

customer_name_6 = "david"
customer_email_6 = "david@email.com"


user_name_1 = "dummy"
user_name_2 = "dumberlina"
user_name_3 = "dumbotron"

user_role = "customer"
# Test data 07/16/20
user_name_4 = "majong"
user_name_5 = "longman"
user_name_6 = "david"

user_role = False
admin_role = True

sticker_name_1 = 'bananas'
img_URL_1 = '#'
price_1 = 2
total_sold_1 = 0

sticker_name_2 = 'cupacakee'
img_URL_2 = '#'
price_2 = 2
total_sold_2 = 0

sticker_name_3 = 'pickles'
img_URL_3 = '#'
price_3 = 3
total_sold_3 = 0

# Jeffrey test data 07/16/20
sticker_name_4 = 'doge'
img_URL_4 = '#'
price_4 = 2.50
total_sold_4 = 1

sticker_name_5 = 'bird'
img_URL_5 = '#'
price_5 = 3.50
total_sold_5 = 5

sticker_name_6 = 'unicorn'
img_URL_6 = '#'
price_6 = 5
total_sold_6 = 3

#############
letter_digits = string.ascii_lowercase + string.digits
order_1 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_1 = '123 Street Ave'
city_1 = 'city_'
state_1 = 'state_'
zipcode_1 = '11111'

order_day_1 = 12
order_month_1 = 1
order_year_1 = 2020

ship_day_1 = 20
ship_month_1 = 1
ship_year_1 = 2020
ship_address_1 = street_name_1 + ' ' + city_1 + ' ' + state_1 + ' ' + zipcode_1
################
order_2 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_2 = '123 city_ Ave'
city_2 = 'Street'
state_2 = 'notCountry'
zipcode_2 = '11111'

order_day_2 = 7
order_month_2 = 7
order_year_2 = 2020

ship_day_2 = 20
ship_month_2 = 7
ship_year_2 = 2020
ship_address_2 = street_name_2 + ' ' + city_2 + ' ' + state_2 + ' ' + zipcode_2
#####################
order_3 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_3 = '123 Berry Rd'
city_3 = 'Straw'
state_3 = 'Berry'
zipcode_3 = '11111'

order_day_3 = 12
order_month_3 = 3
order_year_3 = 2020

ship_day_3 = 20
ship_month_3 = 3
ship_year_3 = 2020
ship_address_3 = street_name_3 + ' ' + city_3 + ' ' + state_3 + ' ' + zipcode_3
################
# Test data 07/16/20
order_4 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_4 = '123 Street Ave'
city_4 = 'city_'
state_4 = 'state_'
zipcode_4 = '11111'

order_day_4 = 20
order_month_4 = 1
order_year_4 = 2020

ship_day_4 = 31
ship_month_4 = 1
ship_year_4 = 2020
ship_address_4 = street_name_4 + ' ' + city_4 + ' ' + state_4 + ' ' + zipcode_4
###################
order_5 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_5 = '456 Street Ave'
city_5 = 'Potato'
state_5 = 'Idaho'
zipcode_5 = '12345'

order_day_5 = 12
order_month_5 = 3
order_year_5 = 2020

ship_day_5 = 20
ship_month_5 = 3
ship_year_5 = 2020
ship_address_5 = street_name_5 + ' ' + city_5 + ' ' + state_5 + ' ' + zipcode_5
######################
# Test for same address as street_name_3 to test for different people ordering at
# same address
order_6 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_6 = '123 Berry Rd'
city_6 = 'Straw'
state_6 = 'Berry'
zipcode_6 = '11111'

order_day_6 = 12
order_month_6 = 3
order_year_6 = 2020

ship_day_6 = 20
ship_month_6 = 3
ship_year_6 = 2020
ship_address_6 = street_name_6 + ' ' + city_6 + ' ' + state_6 + ' ' + zipcode_6
##############
order_7 = ''.join((random.choice(letter_digits) for i in range(12)))
street_name_7 = '123 Street Ave'
city_7 = 'city_'
state_7 = 'state_'
zipcode_7 = '11111'

ship_day_7 = 31
ship_month_7 = 1
ship_year_7 = 2020
ship_address_7 = street_name_7 + ' ' + city_7 + ' ' + state_7 + ' ' + zipcode_7

# #insert customer_orders
# insert_customer_orders_sql = ("""
#     INSERT INTO Customer_Orders (customer_name, customer_email, order_id)
#     VALUES (%s, %s, %s);
# """)
# customer_name_1 = "dummy"
# customer_email_1 = "dummy@email.com"

# customer_name_2 = "dumberlina"
# customer_email_2 = "dumberlina@email.com"

# customer_name_3 = "dumbotron"
# customer_email_3 = "dumbotron@email.com"
# # Test data 07/16/20
# customer_name_4 = "majong"
# customer_email_4 = "majong@email.com"

# customer_name_5 = "longman"
# customer_email_5 = "longman@email.com"

# customer_name_6 = "david"
# customer_email_6 = "david@email.com"

# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_1, customer_email_1, order_1)
# )
# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_2, customer_email_2, order_2)
# )
# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_3, customer_email_3, order_3)
# )
# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_4, customer_email_4, order_4)
# )
# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_5, customer_email_5, order_5)
# )
# cur.execute(
#     insert_customer_orders_sql,
#     (customer_name_6, customer_email_6, order_6)
# )


#insert users
insert_user_sql = ("""
    INSERT INTO Users (mail, user_name, user_role, user_address)
    VALUES (%s, %s, %s, %s) RETURNING user_id
""")

#insert data into Orders
insert_order_sql = ("""
    INSERT INTO Orders (order_id, shipping_address, order_date, user_id,ship_date)
    VALUES (%s, %s, %s, %s, %s);
""")

insert_order_sql_no_order_date = ("""
    INSERT INTO Orders (order_id, shipping_address, user_id)
    VALUES (%s, %s, %s);
""")

# insert data into inventory
insert_inventory_sql = ("""
    INSERT INTO Inventory (sticker_id, quantity)
    VALUES (%s,%s);
""")

#insert data into orders_stickers
insert_order_stickers_sql = ("""
    INSERT INTO Orders_Stickers (order_id, sticker_id, sticker_quantity)
    VALUES (%s, %s, %s);
""")

#insert data into sticker table
#return state_ments return the serial created for the row
insert_sticker_sql = ("""
    INSERT INTO Stickers (sticker_name, img_url, price, total_sold)
    VALUES (%s,%s,%s,%s)
    RETURNING sticker_id;
""")

cur.execute(
    insert_user_sql,
    (customer_email_1, user_name_1, user_role, ship_address_1)
)
user_id1 = cur.fetchone()[0]

cur.execute(
    insert_user_sql,
    (customer_email_2, user_name_2, user_role, ship_address_2)
)
user_id2 = cur.fetchone()[0]

cur.execute(
    insert_user_sql,
    (customer_email_3, user_name_3, user_role, ship_address_3)
)
user_id3 = cur.fetchone()[0]


cur.execute(
    insert_user_sql,
    (customer_email_4, user_name_4, user_role, ship_address_4)
)
user_id4 = cur.fetchone()[0]

cur.execute(
    insert_user_sql,
    (customer_email_5, user_name_5, user_role, ship_address_5)
)
user_id5 = cur.fetchone()[0]

cur.execute(
    insert_user_sql,
    (customer_email_6, user_name_6, admin_role, ship_address_6)
)
user_id6 = cur.fetchone()[0]

cur.execute(
    insert_sticker_sql,
    (sticker_name_1, img_URL_1, price_1, total_sold_1)
)
# grabbing sticker_id for later insertion into inventory and order->sticker
sticker_id1 = cur.fetchone()[0]

cur.execute(
    insert_sticker_sql,
    (sticker_name_2, img_URL_2, price_2, total_sold_2)
)
sticker_id2 = cur.fetchone()[0]

cur.execute(
    insert_sticker_sql,
    (sticker_name_3, img_URL_3, price_3, total_sold_3)
)
sticker_id3 = cur.fetchone()[0]

# New test data 07/16/20
cur.execute(
    insert_sticker_sql,
    (sticker_name_4, img_URL_4, price_4, total_sold_4)
)
sticker_id4 = cur.fetchone()[0]

cur.execute(
    insert_sticker_sql,
    (sticker_name_5, img_URL_5, price_5, total_sold_5)
)
sticker_id5 = cur.fetchone()[0]

cur.execute(
    insert_sticker_sql,
    (sticker_name_6, img_URL_6, price_6, total_sold_6)
)
sticker_id6 = cur.fetchone()[0]


stickerQt1 = 10
cur.execute(insert_inventory_sql, (sticker_id1, stickerQt1))
stickerQt2 = 10
cur.execute(insert_inventory_sql, (sticker_id2, stickerQt2))
stickerQt3 = 10
cur.execute(insert_inventory_sql, (sticker_id3, stickerQt3))
# Test data 07/16/20
stickerQt4 = 0
cur.execute(insert_inventory_sql, (sticker_id4, stickerQt4))

stickerQt5 = 5
cur.execute(insert_inventory_sql, (sticker_id5, stickerQt5))

stickerQt6 = 20
cur.execute(insert_inventory_sql, (sticker_id6, stickerQt6))


cur.execute(
    insert_order_sql,
    (order_1, ship_address_1, datetime.date(order_year_1, order_month_1, order_day_1), 1 ,
    datetime.date(ship_year_1, ship_month_1, ship_day_1))
)

cur.execute(
    insert_order_sql,
    (order_2, ship_address_2, datetime.date(order_year_2, order_month_2, order_day_2), 1 ,
    datetime.date(ship_year_2, ship_month_2, ship_day_2))
)

cur.execute(
    insert_order_sql,
    (order_3, ship_address_3, datetime.date(order_year_3, order_month_3, order_day_3), 1 ,
    datetime.date(ship_year_3, ship_month_3, ship_day_3))
)

# Test data 07/16/20
cur.execute(
    insert_order_sql,
    (order_4, ship_address_4, datetime.date(order_year_4, order_month_4, order_day_4), 1 ,
    datetime.date(ship_year_4, ship_month_4, ship_day_4))
)

cur.execute(
    insert_order_sql,
    (order_5, ship_address_5, datetime.date(order_year_5, order_month_5, order_day_5), 1 ,
    datetime.date(ship_year_5, ship_month_5, ship_day_5))
)

cur.execute(
    insert_order_sql,
    (order_6, ship_address_6, datetime.date(order_year_6, order_month_6, order_day_6), 1 ,
    datetime.date(ship_year_6, ship_month_6, ship_day_6))
)

cur.execute(
    insert_order_sql_no_order_date,
    (order_7, ship_address_7, 1)
)


cur.execute(insert_order_stickers_sql, (order_1, sticker_id1, 2))
cur.execute(insert_order_stickers_sql, (order_1, sticker_id2, 1))

cur.execute(insert_order_stickers_sql, (order_2, sticker_id1, 1))
cur.execute(insert_order_stickers_sql, (order_2, sticker_id3, 1))

cur.execute(insert_order_stickers_sql, (order_3, sticker_id3, 2))
cur.execute(insert_order_stickers_sql, (order_3, sticker_id2, 2))
cur.execute(insert_order_stickers_sql, (order_3, sticker_id1, 2))
# Test data 07/16/20
cur.execute(insert_order_stickers_sql, (order_4, sticker_id2, 5))
cur.execute(insert_order_stickers_sql, (order_4, sticker_id1, 3))

cur.execute(insert_order_stickers_sql, (order_5, sticker_id5, 1))

cur.execute(insert_order_stickers_sql, (order_6, sticker_id1, 1))
cur.execute(insert_order_stickers_sql, (order_6, sticker_id3, 2))
cur.execute(insert_order_stickers_sql, (order_6, sticker_id5, 1))
cur.execute(insert_order_stickers_sql, (order_6, sticker_id6, 2))

conn.commit()