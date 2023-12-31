import sqlite3 as sq
from datetime import datetime


def db_start():
    global db
    global cur

    db = sq.connect('sqlite.db', check_same_thread=False)
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users_info (user_id TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, first_date TEXT, last_date TEXT, role TEXT, phone TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS admins (user_id TEXT, org_name TEXT, phone TEXT, password TEXT, bot_username TEXT, bot_id TEXT PRIMARY KEY)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS service (service_id INTEGER PRIMARY KEY AUTOINCREMENT, service_name TEXT NOT NULL UNIQUE, price REAL, service_hour REAL, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee (employee_id INTEGER, name TEXT NOT NULL, phone TEXT, specialization TEXT, info TEXT, photo BLOB, email TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS register_check (check_regform INTEGER, check_service INTEGER, check_employee INTEGER, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS time_settings (phone TEXT, is_two_graph TEXT, start_time TEXT, end_time TEXT, start_time_two TEXT, end_time_two TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS wekly_settings (phone TEXT, template_one BLOB, template_two BLOB, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS employee_service (phone TEXT,service_name TEXT, bot_username TEXT)")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user_books (record_id INTEGER NOT NULL, user_id TEXT, user_name TEXT, user_phone TEXT, phone_employee TEXT,service_name TEXT,cr_date, TEXT book_date TEXT, comment TEXT, status TEXT, bot_username TEXT)")
    db.commit()


def create_admin(user_id, org_name, phone, password, bot_username, bot_id):
    user = cur.execute("SELECT * FROM admins WHERE bot_id='{key}'".format(key=bot_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO  admins VALUES (?, ?, ?, ?, ?, ?)", (user_id, org_name, phone, password, bot_username, bot_id))
        db.commit()

def create_register_check(bot_username):
    user = cur.execute("SELECT * FROM register_check WHERE bot_username='{key}'".format(key=bot_username)).fetchone()
    if not user:
        cur.execute("INSERT INTO register_check VALUES (?, ?, ?, ?)", (0, 0, 0, bot_username))
        db.commit()

def set_register_check(bot_username, step):
    name_check = 'check_regform'
    if step == 0:
        name_check = 'check_regform'
    elif step == 1:
        name_check = 'check_service'
    elif step == 2:
        name_check = 'check_employee'

    cur.execute("UPDATE register_check SET " + name_check + " = ?  WHERE bot_username = ?", (1, bot_username))
    db.commit()

def get_register_check(bot_username=''):
    register_check = cur.execute("SELECT * FROM register_check WHERE bot_username='{key}'".format(key=bot_username)).fetchone()
    return register_check


def create_service(service_name, price, service_hour=1, bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE service_name='{key}' and bot_username='{key2}'".format(key=service_name, key2=bot_username)).fetchone()
    if not service:
        cur.execute("INSERT INTO service VALUES (?, ?, ?, ?, ?)", (None, service_name, price, service_hour, bot_username))
        db.commit()


def get_service(bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE bot_username='{key}'".format(key=bot_username)).fetchall()
    return service


def delete_service(service_id, bot_username=''):
    try:
        cur.execute("DELETE FROM service WHERE service_id='{key}' and bot_username='{key2}'".format(key=service_id, key2=bot_username))
        db.commit()
    except Exception as err:
        print(err)


def update_service(service_id, service_name, price, service_hour=1, bot_username=''):
    cur.execute(
        "UPDATE service SET service_name = ?, price= ?, service_hour= ?  WHERE service_id = ? and bot_username = ?", (service_name, price, service_hour, service_id , bot_username))
    db.commit()


def create_user(user_id, first_name, last_name, role="USER", phone='', bot_username=''):
    dater = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    user = cur.execute("SELECT * FROM users_info WHERE user_id='{key}' and bot_username= '{key2}'".format(key=user_id, key2=bot_username)).fetchone()
    if not user:
        cur.execute("INSERT INTO  users_info VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, dater, dater, role, phone, bot_username))
        db.commit()
    # else:
    #     update_user_date(user_id, dater, bot_username)


def update_user_date(user_id, dater, bot_username=''):
    cur.execute("UPDATE users_info SET last_date='{key1}' WHERE user_id='{key2}' and bot_username={key3}".format(key1=dater, key2=user_id, key3=bot_username))
    db.commit()

def update_user_phone(user_id, phone, bot_username=''):
    cur.execute("UPDATE users_info SET phone='{}' WHERE user_id='{}' and bot_username={}".format(phone, user_id, bot_username))
    db.commit()

def update_user_role(user_id, role, bot_username=''):
    cur.execute("UPDATE users_info SET role='{}' WHERE user_id='{}' and bot_username={}".format(role, user_id, bot_username))
    db.commit()

def get_service_one(service_id, bot_username=''):
    service = cur.execute("SELECT * FROM service WHERE service_id='{key}' and bot_username='{key2}'".format(key=service_id, key2=bot_username)).fetchone()
    return service

def create_employee(employee_name, phone, specialization, info="", photo="", email="", bot_username=""):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchone()
    if not employee:
        cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (-1, employee_name, phone, specialization, info, photo, email, bot_username))
        db.commit()


def get_employee_all(bot_username=""):
    employee = cur.execute("SELECT * FROM employee where bot_username='{key}'".format(key=bot_username)).fetchall()
    return employee

def get_employee_phone_all(bot_username=""):
    employee = cur.execute("SELECT phone, employee_id FROM employee where bot_username='{key}'".format(key=bot_username)).fetchall()
    return employee

def delete_employee(phone, bot_username=""):
    try:
        cur.execute("DELETE FROM employee WHERE phone='{key}' and bot_username='{key2}' ".format(key=phone, key2=bot_username))
        db.commit()
    except Exception as err:
        print(err)


def update_employee(employee_name, phone, specialization, employee_id=-1, info="", email="", photo="", bot_username=''):
    cur.execute(
        "UPDATE employee SET employee_id = ?, name = ?,specialization= ?, info= ?, photo =?, email=? WHERE phone = ? and bot_username = ?", (employee_id, employee_name, specialization, info, photo, email, phone, bot_username))
    db.commit()

def get_employee_by_phone(phone, bot_username=''):
    employee = cur.execute("SELECT * FROM employee WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchone()
    return employee


def create_time_settings(phone, is_two_graph='off', start_time='00:00', end_time='00:00', start_time_two='00:00', end_time_two='00:00', bot_username=''):
    user = cur.execute("SELECT * FROM time_settings WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchone()
    if not user:
        cur.execute("INSERT INTO  time_settings VALUES (?, ?, ?, ?, ?, ?, ?)", (phone, is_two_graph, start_time, end_time, start_time_two, end_time_two, bot_username))
        db.commit()

def update_time_settings(phone, is_two_graph='off', start_time='00:00', end_time='00:00', start_time_two='00:00', end_time_two='00:00', bot_username=''):
    cur.execute("UPDATE time_settings SET is_two_graph='{}', start_time='{}', end_time='{}', start_time_two='{}', end_time_two='{} WHERE phone='{}' and bot_username={}".format(is_two_graph,start_time, end_time, start_time_two, end_time_two,  phone, bot_username))
    db.commit()
def get_time_settings(phone, bot_username=''):
    user = cur.execute("SELECT * FROM time_settings WHERE phone='{key}' and bot_username='{key2}'".format(key=phone,key2=bot_username)).fetchone()
    return user


def create_wekly_settings(phone, start_date_one, template_one='', start_date_two='', template_two='', bot_username=''):
    cur.execute("INSERT INTO  wekly_settings VALUES (?, ?, ?, ?, ?, ?)", (phone,start_date_one, template_one, start_date_two, template_two, bot_username))
    db.commit()

def update_wekly_settings_one(phone, start_date_one, template_one='', bot_username=''):
    cur.execute("UPDATE wekly_settings SET template_one='{}', start_date_one='{}' WHERE phone='{}' and bot_username='{}'".format(template_one, start_date_one, phone, bot_username))
    db.commit()

def update_wekly_settings_two(phone, start_date_two, template_two='', bot_username=''):
    cur.execute("UPDATE wekly_settings SET template_two='{}', start_date_two='{}' WHERE phone='{}' and bot_username='{}'".format(template_two, start_date_two, phone, bot_username))
    db.commit()
def get_wekly_settings(phone, bot_username=''):
    user = cur.execute("SELECT * FROM wekly_settings WHERE phone='{key}' and bot_username='{key2}'".format(key=phone,key2=bot_username)).fetchone()
    return user

def create_employee_service(phone, service_name_list, bot_username=''):
    employee_service = cur.execute("SELECT * FROM employee_service WHERE phone='{key}' and bot_username='{key2}'".format(key=phone, key2=bot_username)).fetchall()
    if not employee_service:
        for service_name in service_name_list:
            cur.execute("INSERT INTO employee_service VALUES (?, ?, ?)", (phone, service_name, bot_username))
    db.commit()

def delete_employee_service(phone, bot_username=""):
    try:
        cur.execute("DELETE FROM employee_service WHERE phone='{key}' and bot_username='{key2}' ".format(key=phone, key2=bot_username))
        db.commit()
    except Exception as err:
        print(err)

def update_employee_service(phone, service_name_list=[], bot_username=''):
    delete_employee_service(phone, bot_username)
    for service_name in service_name_list:
        cur.execute("INSERT INTO employee_service VALUES (?, ?, ?)", (phone, service_name, bot_username))
    db.commit()

def get_employee_service(phone, bot_username=''):
    service_name_list = cur.execute("SELECT service_name FROM employee_service WHERE phone='{key}' and bot_username='{key2}'".format(key=phone,key2=bot_username)).fetchall()
    fin_list = []
    for service_name in service_name_list:
        fin_list.append(service_name[0])
    return fin_list



def create_user_books(user_id, user_name, user_phone, phone_employee, service_name, cr_date,book_date, comment, status='', bot_username=''):
    cur.execute("INSERT INTO  user_books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (None, user_id, user_name, user_phone, phone_employee, service_name, cr_date,book_date, comment, status, bot_username))
    db.commit()

def update_user_books(record_id, user_id, user_name, user_phone, phone_employee, service_name, cr_date,book_date, comment, status=''):
    cur.execute("UPDATE user_books SET user_id='{}', user_name='{}', user_phone='{}', phone_employee='{}', service_name='{}', cr_date='{}', date='{}', hour='{}', status='{}' WHERE phone='{}'".format(user_id, user_name, user_phone, phone_employee, service_name, cr_date,book_date, comment, status, record_id))
    db.commit()


def get_user_books_by_record(record_id):
    user = cur.execute("SELECT * FROM user_books WHERE record_id='{key}'".format(key=record_id)).fetchone()
    return user


def get_user_books_by_user(user_id, bot_username=''):
    user = cur.execute("SELECT * FROM user_books WHERE user_id='{key}' and bot_username='{key2}'".format(key=user_id, key2=bot_username)).fetchall()
    return user

def get_user_books_by_employee(phone_employee, bot_username=''):
    user = cur.execute("SELECT * FROM user_books WHERE phone_employee='{key}' and bot_username='{key2}'".format(key=phone_employee, key2=bot_username)).fetchall()
    return user