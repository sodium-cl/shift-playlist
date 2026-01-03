import sqlite3
import os
import csv
from datetime import datetime
def create_data_folder():
  data_folder = os.getenv('SHIFT_LIST_DATA_FOLDER', 'shift_list_data')
  data_path = os.path.join(os.getcwd(), data_folder)
  return data_path
def create_db(data_path, user_key):
  data_path = os.path.join(data_path + "/" + user_key)
  os.makedirs(data_path, exist_ok=True)
  db_name = datetime.today().strftime('__data_store_%y%m%d%H%M%S%f') + '.db'
  con = sqlite3.connect(os.path.join(data_path, db_name))
  return con
def create_tables(con):
  cur = con.cursor()
  cur.execute("""
              CREATE TABLE 
              album(service_album_id TEXT PRIMARY KEY,
              album_name TEXT, 
              album_year TEXT, 
              album_type TEXT,
              album_artists TEXT,
              total_tracks INTEGER, 
              release_date TEXT)
              """)
  cur.execute("""
              CREATE TABLE 
              tracks(service_track_id TEXT PRIMARY KEY,
              service_album_id TEXT,
              artists TEXT, 
              track_name TEXT,
              duration_ms INTEGER,
              isrc_id TEXT,
              ean_id TEXT,
              upc_id TEXT,
              FOREIGN KEY(service_album_id) REFERENCES album(service_album_id))
              """)
def insert_album(con, album_data):
  cur = con.cursor()
  print(f"Inserting album:", album_data)
  cur.execute("INSERT OR IGNORE INTO album(service_album_id, album_name, album_year, album_type, album_artists, total_tracks, release_date) VALUES (?, ?, ?, ?, ?, ?, ?)", album_data)
  con.commit()
def insert_track(con, track_data):
  cur = con.cursor()
  print(f"Inserting track:", track_data)
  cur.execute("INSERT OR IGNORE INTO tracks(service_track_id, service_album_id, artists, track_name, duration_ms, isrc_id, ean_id, upc_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", track_data)
  con.commit()
def create_csv(con,data_path):
  cur = con.cursor()
  cur.execute("""
              SELECT track_name,
              duration_ms,
              artists,
              album_name,
              album_year,
              album_type,
              album_artists,
              total_tracks,
              release_date,
              isrc_id,
              ean_id, 
              upc_id FROM album, tracks WHERE tracks.service_album_id = album.service_album_id
              """)
  rows = cur.fetchall()
  csv_dir = os.path.join(data_path, "csv_exports")
  os.makedirs(csv_dir, exist_ok=True)
  csv_file = os.path.join(csv_dir + "/" + datetime.today().strftime('tracks_%y%m%d%H%M%S%f.csv'))
  with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([description[0] for description in cur.description])  # Write headers
      csvwriter.writerows(rows)
def close_db(con):
  con.close()