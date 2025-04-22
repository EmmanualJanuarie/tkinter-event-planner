import sqlite3

conn = sqlite3.connect("eventplanner_db.db")
cur = conn.cursor()

'''execution method to check if table exists in the database if not one's created'''
# UserRegistration
cur.execute("CREATE TABLE IF NOT EXISTS UserRegistration(ID INTEGER PRIMARY KEY, firstname TEXT, lastname TEXT, " \
"email TEXT, isManager INTEGER)")

conn.commit()
conn.close