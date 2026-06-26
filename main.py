# main.py

import sys
import sqlite3

from PyQt5.QtWidgets import QApplication

from boundary.FirstForm import FirstForm


def initDatabase():

    conn = sqlite3.connect(
        "database/photo.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user(

        userid INTEGER PRIMARY KEY AUTOINCREMENT,

        account TEXT UNIQUE,

        password TEXT,

        username TEXT
    )
    """)

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


def main():

    initDatabase()

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Photo Community"
    )

    firstForm = FirstForm()

    firstForm.show()

    sys.exit(
        app.exec_()
    )


if __name__ == "__main__":

    main()