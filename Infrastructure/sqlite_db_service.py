import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "eka.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("DROP TABLE IF EXISTS users")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )"""
        )
        conn.execute(
            """INSERT INTO users (name, email) VALUES
                ('John Doe', 'john.doe@example.com'),
                ('Jane Smith', 'jane.smith@example.com'),
                ('Alice Johnson', 'alice.johnson@example.com')
            """
        )
        conn.commit()
    finally:
        conn.close()


_init_db()


def fetch_users(name):
    print(f"Fetching user with name: {name}")
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name,email FROM users where name LIKE ?',
    (f"%{name}%",))
        result = cursor.fetchone()
        if result:
            name_value, email_value = result
            print(f"Fetched user: {name_value} -> {email_value}")
            return {"found": True, "name": name_value, "email": email_value}

        print("Fetched user: not found")
        return {"found": False, "name": name, "email": None}
    finally:
        conn.close()