import os
import sqlite3
import libsql


DATABASE = "attendance.db"


class TursoCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetchone(self):
        row = self.cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in self.cursor.description]

        return {
            column: value
            for column, value in zip(columns, row)
        }

    def fetchall(self):
        rows = self.cursor.fetchall()

        if not rows:
            return []

        columns = [column[0] for column in self.cursor.description]

        return [
            {
                column: value
                for column, value in zip(columns, row)
            }
            for row in rows
        ]


class TursoConnection:
    def __init__(self):
        url = os.environ.get("TURSO_DATABASE_URL")
        token = os.environ.get("TURSO_AUTH_TOKEN")

        if not url or not token:
            raise RuntimeError(
                "TURSO_DATABASE_URL or TURSO_AUTH_TOKEN is missing."
            )

        self.conn = libsql.connect(
            database=url,
            auth_token=token
        )

    def execute(self, query, parameters=()):
        cursor = self.conn.execute(query, parameters)
        return TursoCursor(cursor)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def get_local_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_db_connection():
    if (
        os.environ.get("TURSO_DATABASE_URL")
        and os.environ.get("TURSO_AUTH_TOKEN")
    ):
        return TursoConnection()

    return get_local_connection()


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