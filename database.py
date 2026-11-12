import sqlite3

DB_NAME = "appointments.db"

def create_database():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            department TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_appointment(patient_name, department, doctor, appointment_date, appointment_time):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments
        (patient_name, department, doctor, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (patient_name, department, doctor, appointment_date, appointment_time, "Booked"))
    appointment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return appointment_id

def get_appointments():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("""
        SELECT id, patient_name, department, doctor,
               appointment_date, appointment_time, status
        FROM appointments ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows
