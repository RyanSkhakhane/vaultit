import random
import sqlite3

DB_PATH = "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                website TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)

def generate_password(length=8):
    chars = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%'
    return ''.join(random.choice(chars) for _ in range(length))

# CREATE
def create_auto_gen(username, website):
    password = generate_password()
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (username, website, password) VALUES (?, ?, ?)",
            (username, website, password)
        )
    return password

def create_manual_gen(username, website, password):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (username, website, password) VALUES (?, ?, ?)",
            (username, website, password)
        )
    return True

# READ
def read_user(username, website):
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? OR website = ?",
            (username, website)
        )
        row = cursor.fetchone()
        return row if row else "Not found"

# UPDATE
def update_pwd_auto_gen(username, website):
    new_password = generate_password()
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE users SET password = ? WHERE username = ? OR website = ?",
            (new_password, username, website)
        )
    return cursor.rowcount > 0

def update_manual_gen(username, website, new_password):
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE users SET password = ? WHERE username = ? OR website = ?",
            (new_password, username, website)
        )
    return cursor.rowcount > 0

# DELETE
def delete_user(username, website):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM users WHERE username = ? AND website = ?",
            (username, website)
        )
    return cursor.rowcount > 0
