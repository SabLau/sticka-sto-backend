import os
import psycopg2
import random
import string
import sys
import codecs
import base64

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message
app = Flask(__name__)
CORS(app)

# os.environ.get returns None if the variable doesn't exist
DATABASE = os.environ.get('STICKA_STO_DB_NAME')
HOST = os.environ.get('STICKA_STO_DB_HOST')
PORT = os.environ.get('STICKA_STO_DB_PORT')
PASSWORD = os.environ.get('STICKA_STO_AD_PW')
USER = os.environ.get('STICKA_STO_USER')

#  app config for flask mail
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = os.getenv('STICKA_STO_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('STICKA_STO_EMAIL_PW')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('STICKA_STO_EMAIL')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASII_ATTACHMENTS'] = False

mail = Mail(app)

conn = psycopg2.connect(
    database=DATABASE,
    host=HOST,
    port=PORT,
    password=PASSWORD,
    user=USER
)

# throw error if the variables do not exist in the environment variables
if not (DATABASE and HOST and PORT and PASSWORD and USER):
    sys.exit("""You have not set all environment variables. Check for:
      * STICKA_STO_DB_NAME
        * STICKA_STO_DB_HOST
        * STICKA_STO_DB_PORT
        * STICKA_STO_AD_PW
        * STICKA_STO_USER """
    )

#checks for optional key inputs
def checkKeys(key, req):
    if key in req.keys():
        return req[key]
    else:
        return None

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/sticker_all", methods=['GET'])
def sticker_all():
    """
    sticker_all reads all the stickers from the url
    ie: 127.0.0.1:5000/sticker_all and queries the database for all stickers

    Parameters:
        None

    Returns:
        returns [
            list of sticker objects (sticker_id, sticker_name, img, price)
        ]
    """

    cur = conn.cursor()

    query = """
        SELECT *
        FROM Stickers
        LEFT JOIN Inventory
        ON Stickers.sticker_id=Inventory.sticker_id
        ORDER BY Stickers.sticker_id
    """
    cur.execute(query)

    res = cur.fetchall()
    all_stickers = []

    for col in res:
        res_dict = {
            "sticker_id": col[0],
            "sticker_name": col[1],
            "img": codecs.decode(col[2]),
            "sticker_price": float(col[3]),
            "sticker_description": col[4],
            "quantity": col[6],

        }
        all_stickers.append(res_dict)

    # Handle if Stickers doesn't exist
    if all_stickers is None:
        return jsonify({
            "result": False,
            "message": "Stickers doesn't exist"
        })
    else:
        return jsonify({
            "result": True,
            "Sticker_list": all_stickers
        })

    return jsonify({
        "result": True,
        "message": "Completed printing all stickers"
    })

    cur.close()


@app.route("/stickers/<sticker_id>", methods=['GET'])
def get_sticker(sticker_id):
    """
    get_sticker takes the sticker_id from the url ie: 127.0.0.1/stickers/1
    and queries the database for the sticker for the given sticker_id

    Parameters:
        sticker_id: the id of the sticker

    Returns:
        returns JSON(sticker_id, sticker_name, img, price)
    """

    cur = conn.cursor()

    query = """
        SELECT *
        FROM Stickers
        JOIN Inventory
        ON Stickers.sticker_id = Inventory.sticker_id
        WHERE Stickers.sticker_id = %s
    """

    cur.execute(query, (sticker_id,))

    res = cur.fetchone()
    res_dict = {
        "sticker_id": res[0],
        "sticker_name": res[1],
        "img": codecs.decode(res[2]),
        "sticker_price": float(res[3]),
        "sticker_description": res[4],
        "quantity": res[6],

    }

    cur.close()

    # Handle if Stickers doesn't exist
    if res is None:
        return jsonify({
            "result": False,
            "message" : "Error, Sticker doesn't exist"
        })
    else:
        return jsonify({
            "result": True,
            "Sticker": res_dict
        })

    return jsonify({
        "result": True,
        "message": "Completed printing sticker information"
    })

@app.route("/create_sticker", methods=['POST'])
def create_sticker():
    """
    create_sticker takes the necessary information from the post request.
    It will run a query to insert that data into the database
    Creates an entry in both Sticker and Inventory tables

    Parameters:
        None
        request.get_json expects (sticker_name, img, price, sticker_description)

    Returns:
        JSON(a string based on success or failure of the insertion)
    """
    req = request.get_json()

    NAME = req['name'] or None
    IMG = req['img'] or None
    PRICE = req['price'] or None
    QUANTITY = req['quantity'] or 0
    STICKER_DESCRIPTION = checkKeys('sticker_description', req)
    

    if (NAME is None or
        IMG is None or
        PRICE is None or
        QUANTITY is None
    ):
        return jsonify({
            "result": False,
            "message": "Missing one or more information."
        })

    cur = conn.cursor()

    sticker_query = """
        INSERT INTO Stickers(sticker_name, img, price, sticker_description)
        VALUES (%s, %s, %s, %s) RETURNING sticker_id
    """
    # Relationship from Stickers(primary_key) -> Inventory(foreign_key)
    inventory_query = """
        INSERT INTO Inventory(sticker_id, quantity)
        VALUES (%s, %s)
    """
    try:
        cur.execute(sticker_query, (NAME, codecs.encode(IMG), PRICE,STICKER_DESCRIPTION))
        sticker_id = cur.fetchone()[0]
        cur.execute(inventory_query, (sticker_id, QUANTITY))
        conn.commit()
        cur.close()
        return jsonify({
            "result": True,
            "message": "Successfully updated database"
        })
    except:
        print("Error in database!")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": "There was an error updating the database."
        })

@app.route("/stickers_update", methods=['PUT'])
def stickers_update():
    """
    stickers_update takes the sticker from the url
    ie: 127.0.0.1:5000/stickers_update and queries the database
    to update the sticker for the given sticker_id

    Parameters:
        sticker_id, sticker_name, img, price, sticker_description

    Returns:
        Success or Error message
    """
    req = request.get_json()

    # TODO: If the post request does not provide adequate information, respond with appropriate error

    STICKER_ID = req['sticker_id'] or None
    NAME = req['sticker_name'] or None
    IMG = req['img'] or None
    PRICE = req['price'] or 0
    QUANTITY = req['quantity'] or 0
    STICKER_DESCRIPTION = checkKeys('sticker_description', req)


    if (STICKER_ID is None or
        NAME is None or
        IMG is None or
        PRICE is None 
    ):
        return jsonify({
            "result": False,
            "message": "Missing one or more information."
        })

    cur = conn.cursor()
    sticker_query = """
        UPDATE Stickers
        SET sticker_name = %s, img = %s, price = %s, sticker_description = %s
        WHERE sticker_id = %s
    """
    
    inventory_query = """
        UPDATE Inventory
        SET quantity = %s
        WHERE sticker_id = %s
    """
    
    try:
        cur.execute(sticker_query, (NAME, IMG, PRICE, STICKER_DESCRIPTION, STICKER_ID))
        cur.execute(inventory_query, (QUANTITY, STICKER_ID))
        conn.commit()
        cur.close()
        return jsonify({
            "result": True,
            "message": "Successfully updated Database"
        })
    except:
        print("Error in database!")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": "Error in Database"
        })



@app.route("/inventory_update", methods=['PUT'])
def inventory_update():
    """
    inventory_update identifies sticker_id then updates.
    It will run a query with parameters of sticker_id to
    update that data into the database.

    Parameters:
        sticker_id (PUT)
        request.get_json expects a new integer quantity

    Returns:
        Success or error message
    """

    # Update to Database
    req = request.get_json()

    QUANTITY = req['quantity']
    STICKER_ID = req['sticker_id']

    cur = conn.cursor()
    query = """
        UPDATE Inventory
        SET quantity = %s
        WHERE sticker_id = %s
    """
    try:
        cur.execute(query, (QUANTITY, STICKER_ID))
        conn.commit()
        cur.close()
        return jsonify({
            "result": True,
            "message": "Successfully updated Database"
        })
    except:
        print("Error in database!")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": "Error in Database"
        })


@app.route("/orders", methods = ['GET'])
def all_orders():
    """
    all_orders reads all the orders from the url
    ie: 127.0.0.1:5000/all_orders and queries the database for all orders

    Parameters:
        None

    Returns:
        returns [
            list of order JSON(order_id, shipping_address, order_date, ship_date)
        ]
    """
    cur = conn.cursor()

    query = """
        SELECT *
        FROM Orders
    """
    cur.execute(query)

    res = cur.fetchall()
    orders = []
    for col in res:
        res_dict = {
            "order_id": col[0],
            "shipping_address": col[1],
            "order_date": col[2],
            "ship_date": col[3],
        }
        orders.append(res_dict)

    # Handle if Orders doesn't exist
    if orders is None:
        return jsonify({
            "result": False,
            "message": "Order doesn't exist."
        })
    else:
        return jsonify({
            "result": True,
            "orders": orders
        })

    return jsonify({
        "result": True,
        "orders": orders
    })

    cur.close()

# Instead of order_id use the generated confirmation code
@app.route("/orders/<order_id>", methods=['GET'])
def get_order(order_id):
    """
    get_order takes the order_id from the url ie: 127.0.0.1/orders/1
    and queries the database for the sticker for the given order_id

    Parameters:
        order_id: the id of the sticker

    Returns:
        returns JSON(order_id, shipping_address, order_date, ship_date)
    """

    cur = conn.cursor()

    query = """
        SELECT *
        FROM Orders
        WHERE order_id = %s
    """

    cur.execute(query, (order_id,))

    res = cur.fetchone()
    res_dict = {
        "order_id": res[0],
        "shipping_address": res[1],
        "order_date": res[2],
        "ship_date": res[3],
    }

    cur.close()

    # Handle if Orders doesn't exist
    if res is None:
        return jsonify({
            "result": False,
            "message": "Order doesn't exist"
        })
    else:
        return jsonify({
            "result": False,
            "order": res_dict
        })

    return jsonify({
        "result": True,
        "message": "Successfully printed out Order"    
    })

# Create a random generated string for the order_id and to send to email
@app.route("/create_order", methods=['POST'])
def create_order():
    """
    create_order takes the necessary information from the post request.
    It will run a query to insert that data into the database
    Creates an entry in Order, Customer_Orders, and Orders_stickers tables

    Parameters:
        None
        request.get_json expects (shipping_address, order_date)

    Returns:
        JSON(a string based on success or failure of the insertion)
    """
    req = request.get_json()

    # TODO: If the post request does not provide adequate information, respond with appropriate error

    # Generate a random generated string
    letter_digits = string.ascii_uppercase + string.digits
    result = ''.join((random.choice(letter_digits) for i in range(12)))

    ORDER = result
    ADDR = req['shipping_address'] or None
    STICKERS_LIST = req['stickers_list'] or None
    USER = req['user_id'] or None

    if (ADDR is None or USER is None):
        return jsonify({
            "result": False,
            "message": "Missing one or more information."
        })

    cur = conn.cursor()

    order_query = """
        INSERT INTO Orders(order_id, shipping_address, user_id)
        VALUES (%s, %s, %s) RETURNING order_id
    """
    # Relationship from Orders -> Orders_Stickers
    Orders_Stickers_query = """
        INSERT INTO Orders_Stickers(order_id, sticker_id, sticker_quantity)
        VALUES (%s, %s, %s)
    """

    try:
        cur.execute(order_query, (ORDER, ADDR, USER))
        order_id = cur.fetchone()[0]
    except:
        print("Error in database! Order ID already exists?")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": """
                There was an error updating the database. Order ID already exists?
            """
        })
    try:

        # Handling adding multiple stickers into one order
        for sticker in STICKERS_LIST:
            cur.execute(
                Orders_Stickers_query,
                (order_id, sticker["id"], sticker["quantity"])
            )

    except:
        print("Error in database! Stickers list?")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": """
                There was an error updating the database. Stickers list?
            """
        })

    try:
        conn.commit()
        cur.close()
        return jsonify({
            "result": True,
            "message": "Successfully updated database"
        })
    except:
        print("Error in database! Connection error?")
        conn.rollback()
        return jsonify({
            "result": False,
            "message": """
                There was an error updating the database. Connection error?
            """
        })

# Endpoint to send emails
# TODO: This hsould not be an endpoint, but a function that is called in
# /create_orders endpoint.
# @app.route("/send_email")
def send_email():

    # Generate a random string consisting of Uppercase letters and numbers
    letter_digits = string.ascii_uppercase + string.digits
    result = ''.join((random.choice(letter_digits) for i in range(12)))

    # TODO: Access user table to grab email and send generated order_id as
    # confirmation code handle cases such that an user email does not exist

    # Subject line of email
    msg = Message('Test',
                recipients = ["name@mail.com"])
    # Email body
    # Grab generated order_id from post_request
    msg.body = 'Here is your confirmation code for your order %s' % (result)
    mail.send(msg)

    return jsonify({"result": True, "message": "Message has been sent!"})

# Endpoint for creating user accounts
@app.route("/account_creation", methods=['POST'])
def create_account():
    """
    create_account adds a new user via POST and run a query to insert that data
    into the database in user and in user_login 

    Parameters:
        None
        request.get_json expects (email, name, is_admin, shipping address, password)
    
    Returns:
        JSON(a string based on success or failure of the insertion)
    """
    req = request.get_json()

    EMAIL = req['email'] or None
    NAME = req['name'] or None
    IS_ADMIN = req['is_admin'] or False
    ADDRESS = checkKeys('shipping_address', req)
    PW = req['password'] or None

    if (
        EMAIL is None or
        NAME is None or
        IS_ADMIN is None or
        PW is None
    ):
        return jsonify({
            "result": False,
            "message": "Missing one or more information."
        })
    
    cur = conn.cursor()

    pw_hash = """
        SELECT crypt(%s, gen_salt('bf', 4))
    """

    user_query = """
        INSERT INTO Users(email, name, is_admin, shipping_address)
        VALUES (%s, %s, %s, %s) RETURNING id
    """

    user_login_query= """
        INSERT INTO user_login (user_id, hashed_password)
        VALUES (%s, %s)
    """

    try:
        cur.execute(pw_hash, (PW,))
        HASHED_PW = cur.fetchone()
        cur.execute(user_query, (EMAIL, NAME, IS_ADMIN, ADDRESS))
        ID = cur.fetchone()[0]
        cur.execute(user_login_query, (ID, HASHED_PW))
        conn.commit()
        cur.close()
        return jsonify({
            "result": True,
            "message": "Successfully updated database"
        })
    except:
        print("Error in database!")
        conn.rollback()
    return jsonify({
        "result": False,
        "message": "There was an error updating the database"
    })

# Endpoint to check admin login credentials
@app.route("/admin_auth", methods=['POST'])
def admin_auth():
    """
    admin_auth checks if a user's login can be verified in the user_login table and if user is admin

    Parameters:
        None
        request.get_json expects (user_email, password)
    Returns:
        JSON(a string based on success or failure of the authentication,
            if the user is an admin,
            what user_id if login is successful)

    """

    req = request.get_json()

    EMAIL = req['email'] or None
    PW = req['password'] or None

    if (
        EMAIL is None or
        PW is None
    ):
        return jsonify({
            "result": False,
            "message": "Missing one or more information."
        })


    cur = conn.cursor()

    admin_query = """
        SELECT is_admin 
        FROM Users 
        WHERE email = %s
    """

    login_query = """
        SELECT (user_login.hashed_password=crypt(%s, user_login.hashed_password)) AS psMatch, Users.id, Users.name
        FROM Users, user_login
        WHERE Users.email=%s AND Users.id=user_login.user_id
    """
    
    try:
        cur.execute(login_query, (PW, EMAIL))
        result=cur.fetchone()
        login_result = result[0]
        userId = result[1]
        name = result[2]
        if login_result:
            cur.execute(admin_query, (EMAIL,))
            isAdmin = cur.fetchone()[0]
            if isAdmin:
                return jsonify({
                    "result": True,
                    "message": "Successfully verified admin login",
                    "isAdmin": isAdmin,
                    "id": userId,
                    "name": name,
                    "email": EMAIL
                })
            else:
                return jsonify({
                    "result": True,
                    "message": "Successfully verified login",
                    "isAdmin": isAdmin,
                    "id": userId,
                    "name": name,
                    "email": EMAIL
                })
        else:
            return jsonify({
                "result": False,
                "message": "Incorrect login information"
            })
    except:
        return jsonify({
            "result": False,
            "message": "There was an error verifying login"
        })                