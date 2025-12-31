# import sqlite3
# from datetime import datetime, date

# DB_PATH = "db/bank.db"


# def _get_connection():
#     return sqlite3.connect(DB_PATH)


# def init_reminder_table():
#     conn = _get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS reminders (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             task TEXT NOT NULL,
#             frequency TEXT NOT NULL,
#             day INTEGER,
#             created_at TIMESTAMP NOT NULL
#         )
#     """)

#     conn.commit()
#     conn.close()


# def add_reminder(user_id: int, task: str, frequency: str, day: int | None = None):
#     init_reminder_table()

#     conn = _get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         INSERT INTO reminders (user_id, task, frequency, day, created_at)
#         VALUES (?, ?, ?, ?, ?)
#     """, (user_id, task, frequency, day, datetime.now()))

#     conn.commit()
#     conn.close()


# def get_reminders(user_id: int):
#     init_reminder_table()

#     conn = _get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT id, task, frequency, day, created_at
#         FROM reminders
#         WHERE user_id = ?
#         ORDER BY created_at DESC
#     """, (user_id,))

#     rows = cur.fetchall()
#     conn.close()
#     return rows


# def delete_reminder(reminder_id: int, user_id: int):
#     conn = _get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         DELETE FROM reminders
#         WHERE id = ? AND user_id = ?
#     """, (reminder_id, user_id))

#     conn.commit()
#     conn.close()


# def get_due_reminders(user_id: int):
#     init_reminder_table()

#     today = date.today()
#     today_day = today.day

#     conn = _get_connection()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT task, frequency, day
#         FROM reminders
#         WHERE user_id = ?
#         AND (
#             frequency = 'daily'
#             OR (frequency = 'monthly' AND day = ?)
#         )
#     """, (user_id, today_day))

#     rows = cur.fetchall()
#     conn.close()
#     return rows





import sqlite3
from datetime import datetime, date

DB_PATH = "db/bank.db"


# -------------------------
# DB CONNECTION
# -------------------------
def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# -------------------------
# TABLE INIT
# -------------------------
def init_reminder_table():
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            frequency TEXT NOT NULL,
            day INTEGER,
            created_at TIMESTAMP NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# ADD REMINDER
# -------------------------
def add_reminder(user_id: int, task: str, frequency: str, day: int | None = None):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reminders (user_id, task, frequency, day, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, task, frequency, day, datetime.now()))

    conn.commit()
    conn.close()


# -------------------------
# GET ALL REMINDERS
# -------------------------
def get_reminders(user_id: int):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task, frequency, day, created_at
        FROM reminders
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------------
# FIND REMINDERS BY TASK (NEW 🔥)
# -------------------------
def find_reminders_by_task(user_id: int, task: str):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task
        FROM reminders
        WHERE user_id = ?
        AND LOWER(task) LIKE ?
    """, (user_id, f"%{task.lower()}%"))

    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------------
# DELETE REMINDER
# -------------------------
def delete_reminder(reminder_id: int, user_id: int):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reminders
        WHERE id = ? AND user_id = ?
    """, (reminder_id, user_id))

    conn.commit()
    conn.close()


# -------------------------
# GET DUE REMINDERS (IN-CHAT NOTIFICATION)
# -------------------------
def get_due_reminders(user_id: int):
    init_reminder_table()

    today = date.today()
    today_day = today.day

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT task, frequency, day
        FROM reminders
        WHERE user_id = ?
        AND (
            frequency = 'daily'
            OR (frequency = 'monthly' AND day = ?)
        )
    """, (user_id, today_day))

    rows = cur.fetchall()
    conn.close()
    return rows
