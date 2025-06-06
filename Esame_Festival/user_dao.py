# *******************************************************
# IMPORTS
# *******************************************************
import sqlite3
from flask_login import current_user

# *******************************************************
# USER OPERATIONS
# *******************************************************
"""
Add the user to the database through the information inserted in the signup form.

:param user_form: the user form containing all the user information
:returns: status of the operation
"""
def add_user(user_form):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO user(name, surname, email, password, type) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(sql, (user_form['name'], user_form['surname'], user_form['email'], user_form['password'], user_form['type']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


"""
Obtain all the info of a user from the database through their respective ID.

:param user_id: the user id used to retrieve info
:returns: the obtained user
"""
def get_user(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, name, surname, email, password, type FROM user WHERE id=?'
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


"""
Obtain all the info of a user from the database through their unique email.

:param user_email: the user email used to retrieve info
:returns: the obtained user
"""
def get_user_by_email(user_email):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, name, surname, email, password, type FROM user WHERE email=?'
    cursor.execute(sql, (user_email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


# *******************************************************
# TICKET OPERATIONS
# *******************************************************
"""
Associates a ticket to a user through the information inserted in the tickets form.

:param ticket_form: the ticket form containing all the ticket information
:returns: status of the operation
"""
def add_ticket_to_user(ticket_form):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO ticket(start_date, type, user_id) VALUES(?,?,?)'
    
    try:
        cursor.execute(sql, (ticket_form["start_date"], ticket_form["type"], current_user.id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


"""
Obtain all the info of a user from the database through their respective ID.

:param user_id: the user id to retrieve the informations of
:returns: the obtained user
"""
def get_ticket_by_user_id(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, start_date, type FROM ticket WHERE user_id=?'
    cursor.execute(sql, (user_id,))
    ticket = cursor.fetchone()

    cursor.close()
    conn.close()

    return ticket