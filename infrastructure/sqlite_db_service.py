import sqlite3
from pathlib import Path

from application.decorators import cached, require_role

DB_PATH = Path(__file__).resolve().parent.parent / "eka.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        # Drop and recreate users table
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

        # Drop and recreate UserCompensation table
        conn.execute("DROP TABLE IF EXISTS user_compensation")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS user_compensation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                base_salary REAL NOT NULL,
                bonus REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )"""
        )
        conn.execute(
            """INSERT INTO user_compensation (user_id, base_salary, bonus) VALUES
                (1, 60000, 5000),
                (2, 80000, 10000),
                (3, 120000, 20000)
            """
        )
        conn.commit()
    finally:
        conn.close()


_init_db()

def db_router(query=None, **kwargs):
    payload = kwargs.copy()
    if isinstance(query, dict):
        payload.update(query)
    elif query is not None:
        payload.setdefault("name", query)

    intent = payload.get("intent", "user")
    role = payload.get("role", "guest")
    name = payload.get("name")

    handlers = {
        "salary": lambda: fetch_users_salary(name=name, role=role),
        "user": lambda: fetch_users(name=name, role=role),
    }
    return handlers.get(intent, handlers["user"])()


@cached(ttl_seconds=300, maxsize=100)
@require_role('admin', 'employee')
def fetch_users(name, role="guest"):
    print(f"Fetching user with name: {name}")
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name,email FROM users where name = ?', (name,))
        result = cursor.fetchone()
        if result:
            name_value, email_value = result
            print(f"Fetched user: {name_value} -> {email_value}")
            return {
                "found": True,
                "name": name_value,
                "email": email_value,
                "suggestions": [],
                "message": "Exact match found"
            }

        cursor.execute('SELECT name,email FROM users where name LIKE ? Limit 5', (f"%{name}%",))

        suggestions = [row[0] for row in cursor.fetchall()]
        if suggestions:
            print(f"Suggestions found: {suggestions}")
            return {
                "found": False,
                "name": None,
                "email": None,
                "suggestions": suggestions,
                "message": "No exact match found, but suggestions are available."
            }

        return {"found": False, "name": None, "email": None, "suggestions": [], "message": "User not found."}
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()


@cached(ttl_seconds=300, maxsize=100)
@require_role('admin')
def fetch_users_salary(name, role="guest"):
    print(f"Fetching user with name: {name}")
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT u.name, uc.base_salary, uc.bonus
                FROM users u
                JOIN user_compensation uc ON u.id = uc.user_id
                WHERE u.name = ?""",
            (name,)
        )
        result = cursor.fetchone()
        if result:
            name_value, base_salary, bonus = result
            return {
                "found": True,
                "name": name_value,
                "compensation": {"base_salary": base_salary, "bonus": bonus},
                "message": "Compensation data retrieved successfully.",
                "authorized": True,
            }
        return {
            "found": False,
            "name": name,
            "compensation": None,
            "message": "No compensation record found.",
            "authorized": True,
        }
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conn.close()