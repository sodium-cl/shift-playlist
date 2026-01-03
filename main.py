import requests
import os
import sqlite3
import data_store.database as datastore

BASE_URL = os.getenv('SPOTIFY_BASE_URL')
ACCESS_TOKEN = os.getenv('SPOTIFY_ACCESS_TOKEN')
LIMIT = 50
OFFSET = 0
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}
con = datastore.create_db()
datastore.create_tables(con)
while True:
    response = requests.get(BASE_URL + 'me/tracks?limit=' + str(LIMIT) + '&offset=' + str(OFFSET), headers=headers)
    if response.status_code == 200:
        data = response.json()
        OFFSET += LIMIT
        for item in data['items']:
            track = item['track']
            album = track['album']
            album_data = (
                album['id'],
                album['name'],
                int(album['release_date'][:4]) if album['release_date_precision'] == 'year' else None,
                album['album_type'],
                ', '.join(artist['name'] for artist in album['artists']),
                album['total_tracks'],
                album['release_date']
            )
            datastore.insert_album(con, album_data)
            track_data = (
                track['id'],
                album['id'],
                ', '.join(artist['name'] for artist in track['artists']),
                track['name'],
                track['duration_ms'],
                track['external_ids'].get('isrc'),
                track['external_ids'].get('ean'),
                track['external_ids'].get('upc'),
            )
            datastore.insert_track(con, track_data)
    if response.status_code == 401:
        print("Access token expired or invalid. Please refresh the token.")
        break
    if not data['next']:
        break
datastore.close_db(con)