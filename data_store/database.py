import sqlite3
from datetime import datetime
def create_db():
  DB_NAME = datetime.today().strftime('__data_store_%y%m%d%H%M%S%f') + ".db"
  con = sqlite3.connect(DB_NAME)
  return con
def create_tables(con):
  cur = con.cursor()
  cur.execute("""
              CREATE TABLE 
              album(album_id TEXT PRIMARY KEY,
              service_album_id TEXT,
              album_name TEXT, 
              album_year TEXT, 
              album_type TEXT,
              album_artists TEXT,
              total_tracks INTEGER, 
              release_date TEXT)
              """)
  cur.execute("""
              CREATE TABLE 
              tracks(track_id TEXT PRIMARY KEY,
              service_track_id TEXT,
              artists TEXT, 
              track_name TEXT,
              duration_ms INTEGER,
              isrc_id TEXT,
              ean_id TEXT,
              upc_id TEXT, 
              service_album_id TEXT,
              FOREIGN KEY(service_album_id) REFERENCES album(service_album_id))
              """)
def insert_album(con, album_data):
  cur = con.cursor()
  print(f"Inserting album:", album_data)
  cur.execute("INSERT INTO album(service_album_id, album_name, album_year, album_type, album_artists, total_tracks, release_date) VALUES (?, ?, ?, ?, ?, ?, ?)", album_data)
  con.commit()
def insert_track(con, track_data):
  cur = con.cursor()
  print(f"Inserting track:", track_data)
  cur.execute("INSERT INTO tracks(service_track_id, artists, track_name, duration_ms, isrc_id, ean_id, upc_id, service_album_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", track_data)
  con.commit()
def close_db(con):
  con.close()