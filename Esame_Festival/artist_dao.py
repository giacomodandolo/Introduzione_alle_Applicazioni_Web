import sqlite3
import datetime

# Operations on artists

"""
Obtain all the info of an artist from 
the database through their respective ID.

:param artist_id: the artist id used to retrieve informations from the database
:returns: the obtained artist
"""
def get_artist(artist_id):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT nome, immagine, descrizione_breve, descrizione FROM artista WHERE id=?'
    cursor.execute(sql, (artist_id,))
    artist = cursor.fetchone()

    cursor.close()
    conn.close()

    return artist

def get_artist_from_name(artist_name):
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nome, immagine, descrizione_breve, descrizione FROM artista WHERE nome=?'
    cursor.execute(sql, (artist_name,))
    artist = cursor.fetchone()

    cursor.close()
    conn.close()

    return artist


"""
Obtain all the info of all the artists from the database.

:returns: the obtained artists
"""
def get_artists():
    conn = sqlite3.connect('db/festival.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT artista.id as id, artista.nome as nome, artista.immagine as immagine, artista.descrizione_breve as descrizione_breve, artista.descrizione as descrizione, inizio, fine, palco.nome as nome_palco, pubblicata FROM artista, performance, palco'
    cursor.execute(sql)
    artist = cursor.fetchall()

    cursor.close()
    conn.close()

    return artist
