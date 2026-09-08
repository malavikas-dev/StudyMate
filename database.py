from multiprocessing.dummy import connection
import sqlite3
from pathlib import Path


# Database location
DATABASE = Path("database/studymate.db")


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    # Create database folder if it doesn't exist
    DATABASE.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    # Allows us to access database columns by name
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    """
    Create all required tables for StudyMate.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # SUBJECTS TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            target_hours REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # -------------------------
    # TASKS TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT NOT NULL,
            estimated_hours REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
        )
    """)


    # -------------------------
    # STUDY SESSIONS TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            duration REAL NOT NULL,
            notes TEXT,

            FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            name TEXT DEFAULT 'Student',
            study_mode TEXT DEFAULT 'Focused Learner',
            daily_goal REAL DEFAULT 3,
            pomodoro_duration INTEGER DEFAULT 25
        )
    """)

    connection.execute("""
        INSERT OR IGNORE INTO settings
        (id, name, study_mode, daily_goal, pomodoro_duration)
        VALUES (1, 'Student', 'Focused Learner', 3, 25)
    """)


    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("StudyMate database created successfully!")