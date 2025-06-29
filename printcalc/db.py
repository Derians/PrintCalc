import sqlite3

DB_FILE = 'sqlite.db'

def get_connection():
    """Get a connection to the SQLite database with row factory enabled"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_spools():
    """Get all spools from the database"""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM spools").fetchall()

def get_spools_by_type(spool_type):
    """Get all spools of a specific type"""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM spools WHERE type = ?", (spool_type,)).fetchall()

def get_spool(spool_id):
    """Get a specific spool by ID"""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM spools WHERE id = ?", (spool_id,)).fetchone()

def add_spool(name, weight, price, spool_type='filament'):
    """Add a new spool to the database"""
    with get_connection() as conn:
        conn.execute("INSERT INTO spools (name, weight, price, type) VALUES (?, ?, ?, ?)", (name, weight, price, spool_type))
        conn.commit()

def update_spool(spool_id, name, weight, price):
    """Update an existing spool"""
    with get_connection() as conn:
        conn.execute("UPDATE spools SET name = ?, weight = ?, price = ? WHERE id = ?", (name, weight, price, spool_id))
        conn.commit()

def delete_spool(spool_id):
    """Delete a spool from the database"""
    with get_connection() as conn:
        conn.execute("DELETE FROM spools WHERE id = ?", (spool_id,))
        conn.commit()

def get_config(key):
    """Get a configuration value by key"""
    with get_connection() as conn:
        row = conn.execute("SELECT value FROM config WHERE key = ?", (key,)).fetchone()
        return float(row[0]) if row else None

def update_config(key, value):
    """Update or insert a configuration value"""
    with get_connection() as conn:
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
