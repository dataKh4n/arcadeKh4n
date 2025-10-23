"""
highscores.py

Enhanced SQLite high-score helper for arcadeKh4n with context manager and error handling.
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import threading
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "highscores.db")
_LOCK = threading.Lock()

class HighScoreDB:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.path, timeout=30)

    def _init_db(self):
        with _LOCK:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS highscores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        player TEXT NOT NULL,
                        score INTEGER NOT NULL,
                        game TEXT NOT NULL,
                        date TEXT NOT NULL
                    )
                    """
                )
                conn.commit()

    def add_score(self, player: str, score: int, game: str) -> None:
        now = datetime.utcnow().isoformat()
        with _LOCK:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO highscores (player, score, game, date) VALUES (?, ?, ?, ?)",
                    (player, int(score), game, now),
                )
                conn.commit()

    def get_top_scores(self, game: Optional[str] = None, limit: int = 10) -> List[Dict[str, str]]:
        with _LOCK:
            with self._connect() as conn:
                cur = conn.cursor()
                if game:
                    cur.execute(
                        "SELECT player, score, game, date FROM highscores WHERE game = ? ORDER BY score DESC, date ASC LIMIT ?",
                        (game, limit),
                    )
                else:
                    cur.execute(
                        "SELECT player, score, game, date FROM highscores ORDER BY score DESC, date ASC LIMIT ?",
                        (limit,),
                    )
                rows = cur.fetchall()
        return [
            {"player": r[0], "score": r[1], "game": r[2], "date": r[3]} for r in rows
        ]

    def get_player_best(self, player: str, game: Optional[str] = None) -> Optional[Dict[str, str]]:
        with _LOCK:
            with self._connect() as conn:
                cur = conn.cursor()
                if game:
                    cur.execute(
                        "SELECT player, score, game, date FROM highscores WHERE player = ? AND game = ? ORDER BY score DESC, date ASC LIMIT 1",
                        (player, game),
                    )
                else:
                    cur.execute(
                        "SELECT player, score, game, date FROM highscores WHERE player = ? ORDER BY score DESC, date ASC LIMIT 1",
                        (player,),
                    )
                row = cur.fetchone()
        if row:
            return {"player": row[0], "score": row[1], "game": row[2], "date": row[3]}
        return None

    def delete_all_scores(self):
        with _LOCK:
            with self._connect() as conn:
                conn.execute("DELETE FROM highscores")
                conn.commit()

    def export_scores(self, file_path: str = "highscores_export.csv") -> None:
        import csv
        rows = self.get_top_scores(limit=1000)
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["player", "score", "game", "date"])
            writer.writeheader()
            writer.writerows(rows)

# Singleton instance for easy import
_db = HighScoreDB()

add_score = _db.add_score
get_top_scores = _db.get_top_scores
get_player_best = _db.get_player_best

def demo():
    print("\n=== arcadeKh4n Highscore Demo ===\n")
    add_score("Alice", 1500, "snake")
    add_score("Bob", 1200, "snake")
    add_score("Charlie", 2000, "quiz")

    print("Top Scores (All Games):")
    for entry in get_top_scores():
        print(f"{entry['player']:<10} {entry['score']:>5} {entry['game']:<10} {entry['date']}")

    print("\nTop Snake Scores:")
    for entry in get_top_scores(game="snake", limit=5):
        print(f"{entry['player']:<10} {entry['score']:>5}")

    print("\nAlice’s Best:", get_player_best("Alice"))

if __name__ == "__main__":
    demo()
