# *******************************************************
# IMPORTS
# *******************************************************
import sqlite3
import user_dao, stage_dao
from datetime import datetime
from flask_login import current_user

# *******************************************************
# CONSTANTS
# *******************************************************
DATES = ["2025-07-18T00:00", "2025-07-19T00:00", "2025-07-20T00:00"]
FORMAT = '%Y-%m-%dT%H:%M'

# *******************************************************
# SUPPORTING FUNCTIONS
# *******************************************************
"""
Obtain the next day.

:param day: day to obtain the next of
:returns: the next day
"""
def get_next_day(day):
    match day:
        case "2025-07-18T00:00":
            return "2025-07-19T00:00"
        case "2025-07-19T00:00":
            return "2025-07-20T00:00"


# *******************************************************
# OPERATIONS ON ARTISTS
# *******************************************************
"""
Obtain all the info of an artist through their respective ID.

:param artist_id: the artist id used to retrieve info
:returns: the obtained artist
"""
def get_artist(artist_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT name, image, short_description, description FROM artist WHERE id=?'
    cursor.execute(sql, (artist_id,))
    artist = cursor.fetchone()

    cursor.close()
    conn.close()

    return artist


"""
Obtain all the info of an artist through their unique name.

:param artist_name: the artist name used to retrieve info
:returns: the obtained artist
"""
def get_artist_from_name(artist_name):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, name, image, short_description, description FROM artist WHERE name=?'
    cursor.execute(sql, (artist_name,))
    artist = cursor.fetchone()

    cursor.close()
    conn.close()

    return artist


# *******************************************************
# OPERATIONS ON PERFORMANCES
# *******************************************************
"""
Add the performance to the database through the information inserted in the performance form.

:param performance_form: the performance form containing all the performance information
:returns: status of the operation
"""
def add_performance(performance_form):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    publish = 1

    success = False
    sql_artist = 'INSERT INTO artist(name, image, short_description, description) VALUES(?,?,?,?)'
    sql_performance = 'INSERT INTO performance(start_date, end_date, music_genre, description, image, published, artist_id, user_id, stage_id) VALUES(?,?,?,?,?,?,?,?,?)'

    if "draft_box" in performance_form:
        publish = 0

    try:
        cursor.execute(sql_artist, (performance_form["name"], performance_form["artist_image"], performance_form["short_description"], performance_form["artist_description"]))
        artist = cursor.lastrowid
        cursor.execute(sql_performance, (performance_form["start_date"], performance_form["end_date"], performance_form["music_genre"], performance_form["performance_description"], performance_form["performance_image"], publish, artist, current_user.id, performance_form["stage"]))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success

"""
Update the performance to the database through the information inserted in the performance form.

:param performance_form: the performance form containing all the performance information
:returns: status of the operation
"""
def update_performance(performance_form, artist_id, overlap):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    publish = 1

    success = False
    sql_artist = 'UPDATE artist SET name=?, short_description=?, description=?, image=? WHERE id=?'
    sql_performance = 'UPDATE performance SET start_date=?, end_date=?, music_genre=?, description=?, image=?, published=?, user_id=?, stage_id=? WHERE artist_id=?'

    if "draft_box" in performance_form or overlap:
        publish = 0

    try:
        cursor.execute(sql_artist, (performance_form["name"], performance_form["short_description"], performance_form["artist_description"], performance_form["artist_image"], artist_id))
        cursor.execute(sql_performance, (performance_form["start_date"], performance_form["end_date"], performance_form["music_genre"], performance_form["performance_description"], performance_form["performance_image"], publish, current_user.id, performance_form["stage"], artist_id))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

    cursor.close()
    conn.close()

    return success


"""
Obtain all the info of the performances.

:returns: the obtained performances
"""
def get_performances():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, start_date, end_date, music_genre, description, image, published, artist_id, user_id, stage_id FROM performance'
    cursor.execute(sql)
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances


"""
Obtain all the info of the performance associated with an artist from the database through the artist ID.

:param artist_id: the artist id used to retrieve informations from the database
:returns: the obtained performance
"""
def get_performance_from_artist(artist_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT start_date, end_date, performance.description as performance_description, performance.image as performance_image, music_genre, published, stage_id, stage.name as stage_name, stage.description as stage_description, stage.image as stage_image, artist_id, artist.name as artist_name, short_description, artist.description as artist_description, artist.image as artist_image, user_id FROM performance, stage, artist WHERE stage_id = stage.id AND artist_id = artist.id AND artist_id=?'
    cursor.execute(sql, (artist_id,))
    performance = cursor.fetchone()

    cursor.close()
    conn.close()

    return performance


"""
Obtain the published performances.

:returns: the published performances
"""
def get_published_performances():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT performance.id as performance_id, performance.description, music_genre, short_description, artist.image as artist_image, start_date, end_date, stage_id, stage.name as stage_name, artist_id, artist.name as artist_name, user_id FROM performance, stage, artist WHERE published = 1 AND stage_id = stage.id AND artist_id = artist.id ORDER BY start_date'
    cursor.execute(sql) 
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances
    

"""
Obtain the unpublished performances of a collaborator.

:param user_id: the collaborator id
:returns: the unpublished performances
"""
def get_unpublished_performances(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT performance.id as performance_id, performance.description, music_genre, short_description, artist.image as artist_image, start_date, end_date, stage_id, stage.name as stage_name, artist_id, artist.name as artist_name, user_id FROM performance, stage, artist WHERE published = 0 AND stage_id = stage.id AND artist_id = artist.id AND user_id = ? ORDER BY start_date'
    cursor.execute(sql, (user_id, ))
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances


"""
Obtain the filtered published performances according to the requested parameters.

:param filters: the filters to apply
:returns: the filtered published performances
"""
def get_published_performances_filter(filters):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    filter_statement = ""
    filter_names = ["start_date", "stage_id", "music_genre"]
        
    for i in range(0, len(filters)):
        if filters[i]:
            match i:
                case 0: # filter date
                    filter_statement += "AND " + filter_names[i] + ">='" + filters[i] + "' "
                    if filters[i] != DATES[2]:
                        filter_statement += "AND " + filter_names[i] + "<'" + get_next_day(filters[i]) + "' "
                case 1: # filter stage
                    filter_statement += "AND " + filter_names[i] + "=" + filters[i] + " "
                case 2: # filter genre
                    filter_statement += "AND " + filter_names[i] + "='" + filters[i] + "' "

    sql = f'SELECT performance.id as performance_id, performance.description, music_genre, short_description, artist.image as artist_image, start_date, end_date, stage_id, stage.name as stage_name, artist_id, artist.name as artist_name, user_id FROM performance, stage, artist WHERE published = 1 AND stage_id = stage.id AND artist_id = artist.id {filter_statement}ORDER BY start_date'
    cursor.execute(sql) 
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances


# *******************************************************
# PERFORMANCE STATISTICS
# *******************************************************
"""
Obtain the quantity of people for each day.

:returns: the list of quantity of people for each day
"""
def get_count_people_days():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT type, start_date FROM ticket'
    cursor.execute(sql)
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    
    people_numbers = [0, 0, 0]
    
    for ticket in tickets:
        match ticket["type"]:
            case 0:
                index = (datetime.strptime(ticket["start_date"], FORMAT) - datetime(2025, 7, 18, 0, 0, 0)).days
                people_numbers[index] = people_numbers[index] + 1
            case 1:
                index = (datetime.strptime(ticket["start_date"], FORMAT) - datetime(2025, 7, 18, 0, 0, 0)).days
                people_numbers[index] = people_numbers[index] + 1
                people_numbers[index + 1] = people_numbers[index + 1] + 1
            case 2:
                people_numbers[0] = people_numbers[0] + 1
                people_numbers[1] = people_numbers[1] + 1
                people_numbers[2] = people_numbers[2] + 1

    return people_numbers


"""
Obtain the quantity of tickets for each type.

:returns: the list of quantity of tickets for each type
"""
def get_tickets_per_type():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT type, start_date FROM ticket'
    cursor.execute(sql)
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    
    ticket_counts = [0, 0, 0]
    
    for ticket in tickets:
        ticket_counts[ticket["type"]] += 1 

    return ticket_counts


# *******************************************************
# OPERATIONS ON MUSIC GENRES
# *******************************************************
"""
Obtain all the distinct music genres.

:returns: the distinct music genres
"""
def get_music_genres():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT DISTINCT music_genre as name FROM performance WHERE published=1'
    cursor.execute(sql)
    music_genres = cursor.fetchall()

    cursor.close()
    conn.close()

    return music_genres
