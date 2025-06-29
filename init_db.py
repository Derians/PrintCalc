import sqlite3
import os

# Database initialization script
DB_FILE = 'sqlite.db'

def init_db():
    # Create a new database if it doesn't exist
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    
    # Create tables
    conn.execute("""
        CREATE TABLE spools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            price REAL NOT NULL,
            type TEXT NOT NULL DEFAULT 'filament'
        )
    """)
    
    conn.execute("""
        CREATE TABLE config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    
    # Insert default configuration
    conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ('energy_price', '0.15'))
    conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ('power_watt', '350'))
    conn.execute("INSERT INTO config (key, value) VALUES (?, ?)", ('markup_multiplier', '1.5'))
    
    # Insert sample materials
    conn.execute("INSERT INTO spools (name, weight, price, type) VALUES (?, ?, ?, ?)", 
                ('PLA White', 1000, 25.0, 'filament'))
    conn.execute("INSERT INTO spools (name, weight, price, type) VALUES (?, ?, ?, ?)", 
                ('PETG Black', 1000, 30.0, 'filament'))
    conn.execute("INSERT INTO spools (name, weight, price, type) VALUES (?, ?, ?, ?)", 
                ('Basic Resin', 1000, 40.0, 'resin'))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
