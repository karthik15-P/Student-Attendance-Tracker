import os
import sqlite3
import libsql_client


# -------------------------------------------------
# Local SQLite connection
# -------------------------------------------------
def get_local_connection():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------------------------
# Turso result wrapper
# -------------------------------------------------
class TursoResult:
    def __init__(self, result):
        self.columns = result.columns
        self.rows = result.rows

    def fetchone(self):
        if not self.rows:
            return None

        row = self.rows[0]

        return {
            column: value
            for column, value in zip(self.columns, row)
        }

    def fetchall(self):
        return [
            {
                column: value
                for column, value in zip(self.columns, row)
            }
            for row in self.rows
        ]


# -------------------------------------------------
# Turso connection wrapper
# -------------------------------------------------
class TursoConnection:
    def __init__(self):
        url = os.environ.get("TURSO_DATABASE_URL")
        token = os.environ.get("TURSO_AUTH_TOKEN")

        if not url:
            raise RuntimeError("TURSO_DATABASE_URL is missing.")

        if not token:
            raise RuntimeError("TURSO_AUTH_TOKEN is missing.")

        self.client = libsql_client.create_client_sync(
            url,
            auth_token=token
        )

    def execute(self, query, parameters=()):
        result = self.client.execute(query, parameters)
        return TursoResult(result)

    def commit(self):
        # Turso executes statements remotely.
        pass

    def close(self):
        self.client.close()


# -------------------------------------------------
# Choose database
# -------------------------------------------------
def get_db_connection():
    turso_url = os.environ.get("TURSO_DATABASE_URL")
    turso_token = os.environ.get("TURSO_AUTH_TOKEN")

    if turso_url and turso_token:
        return TursoConnection()

    # Local development
    return get_local_connection()


# -------------------------------------------------
# Initialize database tables
# -------------------------------------------------
def initialize_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            semester TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            UNIQUE(student_id, date)
        )
    """)

    conn.commit()
    conn.close()