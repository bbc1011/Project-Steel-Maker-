import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS alerted_items (
                item_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                first_alerted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def already_alerted(self, item_id: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM alerted_items WHERE item_id = ?",
            (item_id,),
        ).fetchone()
        return row is not None

    def mark_alerted(self, item_id: str, title: str) -> None:
        self.conn.execute(
            """
            INSERT OR IGNORE INTO alerted_items(item_id, title)
            VALUES (?, ?)
            """,
            (item_id, title),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
