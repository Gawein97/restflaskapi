import sqlite3

with sqlite3.connect("data.db") as connection:
    cursor = connection.cursor()
    create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
    cursor.execute(create_table)
    create_table = "CREATE TABLE IF NOT EXISTS books (name text PRIMARY KEY, author text, pages integer, price real)"
    cursor.execute(create_table)

    cursor.execute("INSERT INTO books VALUES ('Test book', 'test author', 123, 10.99)")

    connection.commit()
