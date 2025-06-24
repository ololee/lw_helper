import sqlite3


def init_db():
    conn = sqlite3.connect('static/db/cache.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cache
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 key TEXT NOT NULL,
                 value TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def save_to_cache(key, value):
    conn = sqlite3.connect('static/db/cache.db')
    c = conn.cursor()
    c.execute("INSERT INTO cache (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def get_from_cache(key):
    conn = sqlite3.connect('static/db/cache.db')
    c = conn.cursor()
    c.execute("SELECT value FROM cache WHERE key = ? ORDER BY timestamp DESC LIMIT 1", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None