import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'nexus100.db')

def init_db():
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'assets'), exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Accounts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                account_id TEXT NOT NULL UNIQUE,
                channel_name TEXT,
                refresh_token TEXT,
                status TEXT DEFAULT 'active',
                last_used TIMESTAMP
            )
        ''')

        # Video Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                video_title TEXT,
                video_path TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            )
        ''')

        # Posting Schedules Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posting_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (video_id) REFERENCES video_logs(id)
            )
        ''')

        # Neural Memory Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS neural_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                niche TEXT NOT NULL UNIQUE,
                strategy TEXT,
                score REAL DEFAULT 5.0,
                encounters INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
