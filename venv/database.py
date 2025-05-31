import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="timetable_app"
    )

def insert_teacher_subject(subject, teacher):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT IGNORE INTO Teachers (name) VALUES (%s)", (teacher,))
    conn.commit()

    cursor.execute("SELECT id FROM Teachers WHERE name = %s", (teacher,))
    teacher_id = cursor.fetchone()[0]

    cursor.execute("INSERT IGNORE INTO Subjects (name, teacher_id) VALUES (%s, %s)", (subject, teacher_id))
    conn.commit()

    cursor.close()
    conn.close()

def fetch_subjects():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Subjects")
    subjects = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return subjects

def init_db():
    # Only use if you're creating tables from Python (optional)
    pass
