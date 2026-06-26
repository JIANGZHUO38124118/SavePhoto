import sqlite3

conn = sqlite3.connect("photo.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS photo(

    photoid INTEGER PRIMARY KEY AUTOINCREMENT,

    filename TEXT,

    filepath TEXT,

    visibility INTEGER,

    owner INTEGER
)
""")

conn.commit()
conn.close()

print("database created")