import os
import sqlite3
import json

DB_FILE = "karata_state.db"

# 🚀 Ensure database and table exist
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_code TEXT PRIMARY KEY,
                state TEXT,
                players TEXT
            )
        ''')
        conn.commit()

# 💾 Save the full game state and players to the DB
def save_game_state(game_code, state: dict, players: dict):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(
            "REPLACE INTO games (game_code, state, players) VALUES (?, ?, ?)",
            (game_code, json.dumps(state), json.dumps(players))
        )
        conn.commit()

# 📦 Load the game state for a given game code
def load_game_state(game_code):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT state, players FROM games WHERE game_code = ?", (game_code,))
        row = c.fetchone()
        if row:
            state = json.loads(row[0])
            players = json.loads(row[1])
            return state, players
        return None

# 📋 List all active game codes (e.g., for lobby view)
def list_games():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT game_code FROM games")
        return [row[0] for row in c.fetchall()]

# 🧹 Optional: Remove a game from the DB
def delete_game(game_code):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM games WHERE game_code = ?", (game_code,))
        conn.commit()
