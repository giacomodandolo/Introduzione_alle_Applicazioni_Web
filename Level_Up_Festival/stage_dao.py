# *******************************************************
# IMPORTS
# *******************************************************
import sqlite3
import datetime

# *******************************************************
# STAGE OPERATIONS
# *******************************************************
"""
Obtain all the info of a stage from the database through their respective ID.

:param stage_id: the stage id used to retrieve informations
:returns: the obtained stage
"""
def get_stage(stage_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, name, description FROM stage WHERE id=?'
    cursor.execute(sql, (stage_id,))
    stage = cursor.fetchone()

    cursor.close()
    conn.close()

    return stage


"""
Obtain all the info for all the stages.

:returns: the obtained stages
"""
def get_stages():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, name, description FROM stage'
    cursor.execute(sql)
    stages = cursor.fetchall()

    cursor.close()
    conn.close()

    return stages