from pathlib import Path
from contextlib import closing
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "eka.db"
MAX_CONTEXT_TURNS = 10

def _init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS conversation_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                user_id TEXT,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        columns = {
            row[1] for row in conn.execute("PRAGMA table_info(conversation_messages)").fetchall()
        }
        if "user_id" not in columns:
            conn.execute("ALTER TABLE conversation_messages ADD COLUMN user_id TEXT")
        conn.execute(
            """CREATE INDEX IF NOT EXISTS idx_conversation_messages_user_id
                ON conversation_messages (user_id, id)"""
        )

_init_db()

def get_conversation_by_user(user_id: str) -> list[dict[str, str]]:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        rows = connection.execute(
            """SELECT role, content FROM conversation_messages
                WHERE user_id = ? ORDER BY id""",
            (user_id,),
        ).fetchall()
    return [{"role": role, "content": content} for role, content in rows]

def get_context_by_user(user_id: str) -> list[dict[str, str]]:
    message_limit = MAX_CONTEXT_TURNS * 2
    with closing(sqlite3.connect(DB_PATH)) as connection:
        rows = connection.execute(
            """SELECT role, content FROM (
                    SELECT id, role, content FROM conversation_messages
                    WHERE user_id = ?
                    ORDER BY id DESC LIMIT ?
                ) ORDER BY id""",
            (user_id, message_limit),
        ).fetchall()
    return [{"role": role, "content": content} for role, content in rows]

def save_conversation_exchange(user_id: str, user_message: str, assistant_message: str):
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.executemany(
            """INSERT INTO conversation_messages (conversation_id, user_id, role, content)
                VALUES (?, ?, ?, ?)""",
            [
                (user_id, user_id, "user", user_message),
                (user_id, user_id, "assistant", assistant_message),
            ],
        )

def clear_conversation_by_user(user_id: str):
    with closing(sqlite3.connect(DB_PATH)) as connection, connection:
        connection.execute(
            "DELETE FROM conversation_messages WHERE user_id = ?",
            (user_id,),
        )
