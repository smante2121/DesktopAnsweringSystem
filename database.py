import sqlite3
# database methods used to send caller info to database

def setup_database(): # Function to set up the database
    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS responses ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        callback_number TEXT,
        is_patient TEXT,
        date_of_birth TEXT,
        gender TEXT,
        state TEXT,
        symptom TEXT
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Function to insert data into the database
def insert_response(callback_number, is_patient, date_of_birth, gender, state, symptom):
    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO responses (callback_number, is_patient, date_of_birth, gender, state, symptom)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (callback_number, is_patient, date_of_birth, gender, state, symptom))
    conn.commit()
    cursor.close()
    conn.close()