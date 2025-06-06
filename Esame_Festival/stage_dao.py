import sqlite3
import datetime

# Operations on stages

"""
Obtain all the info of a stage from the database 
through their respective ID.

:param stage_idd: the stage id used to retrieve informations from the database
:returns: the obtained stage
"""
def get_stage(stage_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nome, descrizione FROM palco WHERE id=?'
    cursor.execute(sql, (stage_id,))
    stage = cursor.fetchone()

    cursor.close()
    conn.close()

    return stage

def get_stages():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nome, descrizione FROM palco'
    cursor.execute(sql)
    stage = cursor.fetchall()

    cursor.close()
    conn.close()

    return stage