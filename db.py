import sqlite3

DB_NAME = "emails.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source TEXT,
                subject TEXT,
                content TEXT,
                summarised INTEGER DEFAULT 0
            )
        """)
        conn.commit()


def store_email(source, subject, content, timestamp):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO emails (timestamp, source, subject, content)
            VALUES (?, ?, ?, ?)
        """, (timestamp, source, subject, content))
        conn.commit()
