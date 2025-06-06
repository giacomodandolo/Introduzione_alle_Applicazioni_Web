import sqlite3
from datetime import datetime
import user_dao, stage_dao, artist_dao
from flask_login import current_user

# DATES
DATES = ["2025-07-18T00:00", "2025-07-19T00:00", "2025-07-20T00:00"]
FORMAT = '%Y-%m-%dT%H:%M'

def get_next_day(day):
    match day:
        case "2025-07-18T00:00":
            return "2025-07-19T00:00"
        case "2025-07-19T00:00":
            return "2025-07-20T00:00"

# Operations on performances

def add_performance(performance_form):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    publish = 1

    success = False
    sql_artist = 'INSERT INTO artista(nome, immagine, descrizione_breve, descrizione) VALUES(?,?,?,?)'
    sql_performance = 'INSERT INTO performance(inizio, fine, genere_musicale, descrizione, immagine, pubblicata, id_artista, id_utente, id_palco) VALUES(?,?,?,?,?,?,?,?,?)'

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
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_performance(performance_form, artist_id, overlap):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    publish = 1

    success = False
    sql_artist = 'UPDATE artista SET nome=?, descrizione_breve=?, descrizione=? WHERE id=?'
    sql_performance = 'UPDATE performance SET inizio=?, fine=?, genere_musicale=?, descrizione=?, pubblicata=?, id_utente=?, id_palco=? WHERE id_artista=?'

    if "draft_box" in performance_form or overlap:
        publish = 0

    try:
        cursor.execute(sql_artist, (performance_form["name"], performance_form["short_description"], performance_form["artist_description"], artist_id))
        cursor.execute(sql_performance, (performance_form["start_date"], performance_form["end_date"], performance_form["music_genre"], performance_form["performance_description"], publish, current_user.id, performance_form["stage"], artist_id))
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
Obtain all the info of the performance associated with an artist
from the database through their respective ID.

:param artist_id: the artist id used to retrieve informations from the database
:returns: the obtained performance, stage and collaborator
"""
def get_performances():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT descrizione, genere_musicale, pubblicata, immagine, inizio, fine, id_palco, id_utente FROM performance ORDER BY inizio'
    cursor.execute(sql)
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances

"""
Obtain all the info of the performance associated with an artist
from the database through their respective ID.

:param artist_id: the artist id used to retrieve informations from the database
:returns: the obtained performance, stage and collaborator
"""
def get_performance_from_artist(artist_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT performance.descrizione as performance_description, genere_musicale, pubblicata, performance.immagine as performance_image, inizio, fine, id_palco, palco.nome as palco_nome, id_utente, artista.nome as artist_name, descrizione_breve, artista.descrizione as artist_description, artista.immagine as artist_image, id_artista FROM performance, palco, artista WHERE id_palco = palco.id AND id_artista = artista.id AND id_artista=?'
    cursor.execute(sql, (artist_id,))
    performance = cursor.fetchone()

    cursor.close()
    conn.close()

    return performance

def get_people_count_days():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT tipologia, giorno_inizio FROM biglietto'
    cursor.execute(sql)
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    
    ticket_counts = [0, 0, 0]
    
    for ticket in tickets:
        match ticket["tipologia"]:
            case 0:
                index = (datetime.strptime(ticket["giorno_inizio"], FORMAT) - datetime(2025, 7, 18, 0, 0, 0)).days
                ticket_counts[index] = ticket_counts[index] + 1
            case 1:
                index = (datetime.strptime(ticket["giorno_inizio"], FORMAT) - datetime(2025, 7, 18, 0, 0, 0)).days
                ticket_counts[index] = ticket_counts[index] + 1
                ticket_counts[index + 1] = ticket_counts[index + 1] + 1
            case 2:
                ticket_counts[0] = ticket_counts[0] + 1
                ticket_counts[1] = ticket_counts[1] + 1
                ticket_counts[2] = ticket_counts[2] + 1

    return ticket_counts

def get_tickets_per_type():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT tipologia, giorno_inizio FROM biglietto'
    cursor.execute(sql)
    tickets = cursor.fetchall()

    cursor.close()
    conn.close()
    
    ticket_counts = [0, 0, 0]
    
    for ticket in tickets:
        ticket_counts[ticket["tipologia"]] += 1 

    return ticket_counts


def get_published_performances():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT performance.descrizione, genere_musicale, descrizione_breve, artista.immagine as artist_image, inizio, fine, palco.nome as stage_name, id_artista, artista.nome as artist_name, id_utente FROM performance, palco, artista WHERE pubblicata = 1 AND id_palco = palco.id AND id_artista = artista.id ORDER BY inizio'
    cursor.execute(sql) 
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances
    

def get_unpublished_performances(user_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT performance.descrizione, genere_musicale, descrizione_breve, artista.immagine as artist_image, inizio, fine, palco.nome as stage_name, id_artista, artista.nome as artist_name, id_utente FROM performance, palco, artista WHERE pubblicata = 0 AND id_palco = palco.id AND id_artista = artista.id AND id_utente=?'
    cursor.execute(sql, (user_id, ))
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances

def get_music_genres():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT DISTINCT genere_musicale FROM performance WHERE pubblicata=1'
    cursor.execute(sql) 
    music_genres = cursor.fetchall()

    cursor.close()
    conn.close()

    return music_genres

def get_published_performances_filter(filters):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    filter_statement = ""
    filter_names = ["inizio", "id_palco", "genere_musicale"]
    
    print(filters)
    
    for i in range(0, len(filters)):
        print(filters[i], filter_statement)
        if filters[i]:
            match i:
                case 0: # filter date
                    filter_statement += "AND " + filter_names[i] + ">='" + filters[i] + "' "
                    if filters[i] != DATES[2]:
                        filter_statement += "AND " + filter_names[i] + "<'" + get_next_day(filters[i]) + "' "
                case 1: # filter stage
                    filter_statement += "AND " + filter_names[i] + "= " + filters[i] + " "
                case 2: # filter genre
                    filter_statement += "AND " + filter_names[i] + "= '" + filters[i] + "' "

            
    
    sql = f'SELECT performance.descrizione, genere_musicale, descrizione_breve, artista.immagine as artist_image, inizio, fine, palco.nome as stage_name, id_artista, artista.nome as artist_name, id_utente FROM performance, palco, artista WHERE pubblicata = 1 AND id_palco = palco.id AND id_artista = artista.id {filter_statement}ORDER BY inizio'
    print(sql)
    cursor.execute(sql) 
    performances = cursor.fetchall()

    cursor.close()
    conn.close()

    return performances
