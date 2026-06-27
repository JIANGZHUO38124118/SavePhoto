import sqlite3

conn = sqlite3.connect("database/photo.db")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS parameter(
    parameterid INTEGER PRIMARY KEY AUTOINCREMENT,
    photoid INTEGER,
    name TEXT,
    value TEXT
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        userid INTEGER,
        photoid INTEGER,
        PRIMARY KEY (userid, photoid),
        FOREIGN KEY (userid) REFERENCES user(userid) ON DELETE CASCADE,
        FOREIGN KEY (photoid) REFERENCES photo(photoid) ON DELETE CASCADE
    );
""")

conn.commit()
conn.close()

print("database created")