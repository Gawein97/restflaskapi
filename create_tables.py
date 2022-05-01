import sqlite3

with sqlite3.connect("data.db") as connection:
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(create_table)
    connection.commit()