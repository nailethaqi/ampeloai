from pathlib import Path
import sqlite3
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "analysis.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_analysis(predicted_class, confidence):
    connection = get_connection()

    cursor = connection.cursor()

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute(
        """
        INSERT INTO analyses (
            predicted_class,
            confidence,
            created_at
        )
        VALUES (?, ?, ?)
        """,
        (
            predicted_class,
            confidence,
            created_at
        )
    )

    connection.commit()
    connection.close()


def get_history(limit=50):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            predicted_class,
            confidence,
            created_at
        FROM analyses
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def get_statistics():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM analyses
        """
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT
            predicted_class,
            COUNT(*) AS count
        FROM analyses
        GROUP BY predicted_class
        """
    )

    rows = cursor.fetchall()

    connection.close()

    counts = {
        "Black_Rot": 0,
        "Esca": 0,
        "Healthy": 0,
        "Leaf_Blight": 0
    }

    for row in rows:
        counts[row["predicted_class"]] = row["count"]

    return {
        "total_analyses": total,
        "classes": counts
    }