import sqlite3
from datetime import datetime

from flask_login import current_user

# Operations on users

def add_user(user_form):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utente(nome, cognome, email, password, tipologia) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(sql, (user_form['name'], user_form['surname'], user_form['email'], user_form['password'], user_form['type']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def add_ticket_to_user(ticket):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO biglietto(giorno_inizio, tipologia, utente_id) VALUES(?,?,?)'
    
    try:
        cursor.execute(sql, (ticket["start_date"], ticket["type"], current_user.id))
        
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


"""
Obtain all the info of a user from the database 
through their respective ID.

:param user_id: the user id used to retrieve informations from the database
:returns: the obtained user
"""
def get_user(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nome, cognome, email, password, tipologia FROM utente WHERE id=?'
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_email(user_email):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nome, cognome, email, password, tipologia FROM utente WHERE email=?'
    cursor.execute(sql, (user_email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_ticket_by_user_id(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, giorno_inizio, tipologia FROM biglietto WHERE utente_id=?'
    cursor.execute(sql, (user_id,))
    ticket = cursor.fetchone()

    cursor.close()
    conn.close()

    return ticket