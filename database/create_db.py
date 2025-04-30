import sqlite3

# Connect to database
conn = sqlite3.connect("events.db")
cursor = conn.cursor()

 # Create UserRegistration table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS UserRegistration (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT,
        lastname TEXT,
        email TEXT UNIQUE,
        isManager INTEGER,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    
# Create the events table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    description TEXT
)
""")
conn.commit()

def save_event_to_db(title, date, time, location, description):
    cursor.execute(
        "INSERT INTO events (title, date, time, location, description) VALUES (?, ?, ?, ?, ?)",
        (title, date, time, location, description)
    )
    conn.commit()

def search_event_by_title(title):
    cursor.execute("SELECT * FROM events WHERE LOWER(title)=?", (title.lower(),))
    return cursor.fetchone()

def get_all_events():
    cursor.execute("SELECT title, date, time, location, description FROM events")
    return cursor.fetchall()

