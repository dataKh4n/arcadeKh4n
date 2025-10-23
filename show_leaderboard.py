# show_leaderboard.py
# Shows top scores (per-game and overall)

import sqlite3
from pathlib import Path

DB = Path(__file__).parent / 'highscores.db'

def get_games():
    if not DB.exists():
        return []
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT game FROM highscores')
        rows = cur.fetchall()
    return [r[0] for r in rows]

def show_top(game=None, limit=10):
    if not DB.exists():
        print('No highscores.db found — play a game to create it.')
        return
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if game:
            cur.execute('SELECT player, score, date FROM highscores WHERE game = ? ORDER BY score DESC, date ASC LIMIT ?', (game, limit))
        else:
            cur.execute('SELECT player, score, game, date FROM highscores ORDER BY score DESC, date ASC LIMIT ?', (limit,))
        rows = cur.fetchall()

    if not rows:
        print('No scores found.')
        return

    if game:
        print(f'=== Top {limit} for {game} ===')
        for r in rows:
            print(f'{r[0]:<12} {r[1]:>6}  {r[2]}')
    else:
        print(f'=== Top {limit} (All games) ===')
        for r in rows:
            print(f'{r[0]:<12} {r[1]:>6}  {r[2]:<18} {r[3]}')

if __name__ == '__main__':
    games = get_games()
    if not games:
        print('No games with scores yet.')
    else:
        print('Games with scores:')
        for i, g in enumerate(games, 1):
            print(f'{i}. {g}')
        print('\nOverall top scores:')
        show_top(limit=10)
        print('\nEnter a game name to view its top scores (or press Enter to exit):')
        choice = input().strip()
        if choice:
            show_top(game=choice, limit=20)
