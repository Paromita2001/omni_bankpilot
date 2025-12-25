import sqlite3
from pathlib import Path

# -------------------------
# Database path
# -------------------------
DB_PATH = Path(__file__).parent / "bank.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------
# Create Tables
# -------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ACCOUNTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        account_number TEXT,
        balance REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # BENEFICIARIES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beneficiaries (
        beneficiary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # TRANSACTIONS (simple: kisko, kitna, kab)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        transaction_type TEXT,
        description TEXT,
        trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    # REMINDERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        reminder_text TEXT,
        reminder_time TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully")


# -------------------------
# Insert Sample Users
# -------------------------
def insert_users():
    conn = get_connection()
    cursor = conn.cursor()

    users = [
        ("Paromita Karmakar", "7205013256", "paro@example.com", "paro@1234"),
        ("Rahul Sharma", "9988776655", "rahul.sharma@example.com", "rahul@1234"),
        ("Aditi Mehra", "9123456780", "aditi.mehra@example.com", "aditi@1234"),
        ("Vikram Singh", "9876501234", "vikram.singh@example.com", "vikram@1234"),
        ("Sana Khan", "9090909090", "sana.khan@example.com", "sana@1234"),
        ("Karan Patel", "9911223344", "karan.patel@example.com", "karan@1234"),
        ("Riya Verma", "9876123450", "riya.verma@example.com", "riya@1234"),
        ("Arjun Nair", "9812345678", "arjun.nair@example.com", "arjun@1234"),
        ("Neha Joshi", "9001122334", "neha.joshi@example.com", "neha@1234"),
        ("Mohit Gupta", "9898989898", "mohit.gupta@example.com", "mohit@1234")
    ]

    cursor.executemany("""
    INSERT INTO users (name, phone, email, password_hash)
    VALUES (?, ?, ?, ?)
    """, users)

    conn.commit()
    conn.close()
    print("✅ Users inserted")


# -------------------------
# Insert Accounts
# -------------------------
def insert_accounts():
    conn = get_connection()
    cursor = conn.cursor()

    accounts = [
        (1, "ACC11223344", 52000.00),
        (2, "ACC22334455", 150000.50),
        (3, "ACC33445566", 84500.75),
        (4, "ACC44556677", 126000.00),
        (5, "ACC55667788", 43000.25),
        (6, "ACC66778899", 99000.00),
        (7, "ACC77889900", 25000.00),
        (8, "ACC88990011", 178500.40),
        (9, "ACC99001122", 76000.00),
        (10, "ACC10111213", 60500.95)
    ]

    cursor.executemany("""
    INSERT INTO accounts (user_id, account_number, balance)
    VALUES (?, ?, ?)
    """, accounts)

    conn.commit()
    conn.close()
    print("✅ Accounts inserted")


# -------------------------
# Insert Beneficiaries
# -------------------------
def insert_beneficiaries():
    conn = get_connection()
    cursor = conn.cursor()

    beneficiaries = [
        # User 1
        (1, "Rohit Sharma", "9000000001"),
        (1, "Aman Verma", "9000000002"),
        (1, "Simran Kaur", "9000000003"),
        (1, "Neha Kapoor", "9000000004"),
        (1, "Kiran Patel", "9000000005"),
        (1, "Vikas Mehta", "9000000006"),
        (1, "Pooja Singh", "9000000007"),
        (1, "Dev Mishra", "9000000008"),
        (1, "Sonia Arora", "9000000009"),
        (1, "Arjun Malhotra", "9000000010"),

        # User 2
        (2, "Riya Malhotra", "9000000011"),
        (2, "Tarun Sinha", "9000000012"),
        (2, "Aditi Rao", "9000000013"),
        (2, "Harsh Vardhan", "9000000014"),
        (2, "Sneha Jain", "9000000015"),
        (2, "Kunal Gupta", "9000000016"),
        (2, "Komal Sharma", "9000000017"),
        (2, "Nikhil Bansal", "9000000018"),
        (2, "Jaya Patel", "9000000019"),
        (2, "Sunil Yadav", "9000000020"),

        # User 3
        (3, "Meena Kumari", "9000000021"),
        (3, "Suresh Nair", "9000000022"),
        (3, "Anil Kumar", "9000000023"),
        (3, "Fatima Syed", "9000000024"),
        (3, "Ritu Saxena", "9000000025"),
        (3, "Rajesh Khanna", "9000000026"),
        (3, "Priya Das", "9000000027"),
        (3, "Imran Ali", "9000000028"),
        (3, "Krishna Rao", "9000000029"),
        (3, "Arpita Bose", "9000000030"),

        # User 4
        (4, "Deepak Yadav", "9000000031"),
        (4, "Shalini Gupta", "9000000032"),
        (4, "Gaurav Singh", "9000000033"),
        (4, "Tanya Kapoor", "9000000034"),
        (4, "Sahil Khan", "9000000035"),
        (4, "Lavanya Iyer", "9000000036"),
        (4, "Yash Raj", "9000000037"),
        (4, "Preeti Nair", "9000000038"),
        (4, "Ashwin Rao", "9000000039"),
        (4, "Monika Jain", "9000000040"),

        # User 5
        (5, "Kabir Mehta", "9000000041"),
        (5, "Ishita Sharma", "9000000042"),
        (5, "Rohan Joshi", "9000000043"),
        (5, "Snehal Patil", "9000000044"),
        (5, "Aditya Deshmukh", "9000000045"),
        (5, "Sana Sheikh", "9000000046"),
        (5, "Farhan Ali", "9000000047"),
        (5, "Namrata Bose", "9000000048"),
        (5, "Jatin Patel", "9000000049"),
        (5, "Bhavya Sethi", "9000000050"),

        # User 6
        (6, "Varun Singh", "9000000051"),
        (6, "Chirag Shah", "9000000052"),
        (6, "Aisha Khan", "9000000053"),
        (6, "Ritesh Kumar", "9000000054"),
        (6, "Pallavi Roy", "9000000055"),
        (6, "Omar Shaikh", "9000000056"),
        (6, "Shreya Rathi", "9000000057"),
        (6, "Harshit Garg", "9000000058"),
        (6, "Tara Menon", "9000000059"),
        (6, "Naveen Rao", "9000000060"),

        # User 7
        (7, "Yuvraj Singh", "9000000061"),
        (7, "Mahima Jain", "9000000062"),
        (7, "Siddharth Mehra", "9000000063"),
        (7, "Payal Arora", "9000000064"),
        (7, "Aman Ali", "9000000065"),
        (7, "Rashmi Das", "9000000066"),
        (7, "Vikrant Nair", "9000000067"),
        (7, "Tanvi Shah", "9000000068"),
        (7, "Hemant Yadav", "9000000069"),
        (7, "Shruti Verma", "9000000070"),

        # User 8
        (8, "Parth Malhotra", "9000000071"),
        (8, "Jasmine Kaur", "9000000072"),
        (8, "Mohit Sinha", "9000000073"),
        (8, "Aarohi Gupta", "9000000074"),
        (8, "Tejas Desai", "9000000075"),
        (8, "Ayaan Khan", "9000000076"),
        (8, "Bhavika Patel", "9000000077"),
        (8, "Rehan Shaikh", "9000000078"),
        (8, "Nidhi Sharma", "9000000079"),
        (8, "Samar Kapoor", "9000000080"),

        # User 9
        (9, "Kartik Mathur", "9000000081"),
        (9, "Manisha Iyer", "9000000082"),
        (9, "Saurabh Saxena", "9000000083"),
        (9, "Poonam Kumari", "9000000084"),
        (9, "Abdul Rahman", "9000000085"),
        (9, "Vidhi Gupta", "9000000086"),
        (9, "Raghav Sharma", "9000000087"),
        (9, "Ishan Patel", "9000000088"),
        (9, "Trisha Bose", "9000000089"),
        (9, "Devanshi Mehta", "9000000090"),

        # User 10
        (10, "Ananya Singh", "9000000091"),
        (10, "Harshil Shah", "9000000092"),
        (10, "Meera Rao", "9000000093"),
        (10, "Krish Patel", "9000000094"),
        (10, "Shivani Sharma", "9000000095"),
        (10, "Ravish Kumar", "9000000096"),
        (10, "Ayushi Jain", "9000000097"),
        (10, "Karan Malhotra", "9000000098"),
        (10, "Surbhi Thakur", "9000000099"),
        (10, "Aniket Deshmukh", "9000000100")
    ]

    cursor.executemany("""
    INSERT INTO beneficiaries (user_id, name, phone_number)
    VALUES (?, ?, ?)
    """, beneficiaries)

    conn.commit()
    conn.close()
    print("✅ Beneficiaries inserted for all 10 users")



# -------------------------
# Insert 10 Sample Transactions
# -------------------------
def insert_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    transactions = [
        # User 1
        (1, -600, "debit", "Rohit Sharma"),
        (1, -1200, "debit", "Aman Verma"),
        (1, -450, "debit", "Simran Kaur"),
        (1, -900, "debit", "Neha Kapoor"),
        (1, -750, "debit", "Kiran Patel"),
        (1, -1300, "debit", "Vikas Mehta"),
        (1, -500, "debit", "Pooja Singh"),
        (1, -1100, "debit", "Dev Mishra"),
        (1, -650, "debit", "Sonia Arora"),
        (1, -1600, "debit", "Arjun Malhotra"),

        # User 2
        (2, -900, "debit", "Riya Malhotra"),
        (2, -1500, "debit", "Tarun Sinha"),
        (2, -700, "debit", "Aditi Rao"),
        (2, -1400, "debit", "Harsh Vardhan"),
        (2, -650, "debit", "Sneha Jain"),
        (2, -1800, "debit", "Kunal Gupta"),
        (2, -550, "debit", "Komal Sharma"),
        (2, -1000, "debit", "Nikhil Bansal"),
        (2, -1300, "debit", "Jaya Patel"),
        (2, -1200, "debit", "Sunil Yadav"),

        # User 3
        (3, -700, "debit", "Meena Kumari"),
        (3, -1600, "debit", "Suresh Nair"),
        (3, -800, "debit", "Anil Kumar"),
        (3, -950, "debit", "Fatima Syed"),
        (3, -400, "debit", "Ritu Saxena"),
        (3, -1300, "debit", "Rajesh Khanna"),
        (3, -600, "debit", "Priya Das"),
        (3, -900, "debit", "Imran Ali"),
        (3, -1100, "debit", "Krishna Rao"),
        (3, -1500, "debit", "Arpita Bose"),

        # User 4
        (4, -500, "debit", "Deepak Yadav"),
        (4, -900, "debit", "Shalini Gupta"),
        (4, -1200, "debit", "Gaurav Singh"),
        (4, -1400, "debit", "Tanya Kapoor"),
        (4, -700, "debit", "Sahil Khan"),
        (4, -1600, "debit", "Lavanya Iyer"),
        (4, -900, "debit", "Yash Raj"),
        (4, -1000, "debit", "Preeti Nair"),
        (4, -1300, "debit", "Ashwin Rao"),
        (4, -850, "debit", "Monika Jain"),

        # User 5
        (5, -1000, "debit", "Kabir Mehta"),
        (5, -1400, "debit", "Ishita Sharma"),
        (5, -600, "debit", "Rohan Joshi"),
        (5, -900, "debit", "Snehal Patil"),
        (5, -1500, "debit", "Aditya Deshmukh"),
        (5, -700, "debit", "Sana Sheikh"),
        (5, -1200, "debit", "Farhan Ali"),
        (5, -450, "debit", "Namrata Bose"),
        (5, -800, "debit", "Jatin Patel"),
        (5, -1100, "debit", "Bhavya Sethi"),

        # User 6
        (6, -900, "debit", "Varun Singh"),
        (6, -1400, "debit", "Chirag Shah"),
        (6, -700, "debit", "Aisha Khan"),
        (6, -1300, "debit", "Ritesh Kumar"),
        (6, -600, "debit", "Pallavi Roy"),
        (6, -1100, "debit", "Omar Shaikh"),
        (6, -500, "debit", "Shreya Rathi"),
        (6, -950, "debit", "Harshit Garg"),
        (6, -800, "debit", "Tara Menon"),
        (6, -1500, "debit", "Naveen Rao"),

        # User 7
        (7, -650, "debit", "Yuvraj Singh"),
        (7, -1200, "debit", "Mahima Jain"),
        (7, -900, "debit", "Siddharth Mehra"),
        (7, -450, "debit", "Payal Arora"),
        (7, -700, "debit", "Aman Ali"),
        (7, -800, "debit", "Rashmi Das"),
        (7, -1400, "debit", "Vikrant Nair"),
        (7, -500, "debit", "Tanvi Shah"),
        (7, -1000, "debit", "Hemant Yadav"),
        (7, -1500, "debit", "Shruti Verma"),

        # User 8
        (8, -1100, "debit", "Parth Malhotra"),
        (8, -600, "debit", "Jasmine Kaur"),
        (8, -900, "debit", "Mohit Sinha"),
        (8, -1300, "debit", "Aarohi Gupta"),
        (8, -1500, "debit", "Tejas Desai"),
        (8, -700, "debit", "Ayaan Khan"),
        (8, -1200, "debit", "Bhavika Patel"),
        (8, -800, "debit", "Rehan Shaikh"),
        (8, -950, "debit", "Nidhi Sharma"),
        (8, -1400, "debit", "Samar Kapoor"),

        # User 9
        (9, -1200, "debit", "Kartik Mathur"),
        (9, -900, "debit", "Manisha Iyer"),
        (9, -700, "debit", "Saurabh Saxena"),
        (9, -1400, "debit", "Poonam Kumari"),
        (9, -800, "debit", "Abdul Rahman"),
        (9, -1100, "debit", "Vidhi Gupta"),
        (9, -1500, "debit", "Raghav Sharma"),
        (9, -600, "debit", "Ishan Patel"),
        (9, -1000, "debit", "Trisha Bose"),
        (9, -450, "debit", "Devanshi Mehta"),

        # User 10
        (10, -900, "debit", "Ananya Singh"),
        (10, -1500, "debit", "Harshil Shah"),
        (10, -700, "debit", "Meera Rao"),
        (10, -1100, "debit", "Krish Patel"),
        (10, -800, "debit", "Shivani Sharma"),
        (10, -1200, "debit", "Ravish Kumar"),
        (10, -500, "debit", "Ayushi Jain"),
        (10, -1400, "debit", "Karan Malhotra"),
        (10, -1000, "debit", "Surbhi Thakur"),
        (10, -600, "debit", "Aniket Deshmukh")
    ]

    cursor.executemany("""
    INSERT INTO transactions (user_id, amount, transaction_type, description)
    VALUES (?, ?, ?, ?)
    """, transactions)

    conn.commit()
    conn.close()
    print("✅ Transactions inserted for all 10 users")



def get_transaction_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT description, amount, trans_date
    FROM transactions
    WHERE user_id = ?
    ORDER BY trans_date DESC
    LIMIT 10
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_id, name, password_hash
    FROM users
    WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None, "❌ User not found"

    user_id, name, stored_password = user

    # simple password check (as per your current DB)
    if stored_password == password:
        return user_id, f"✅ Login successful. Welcome {name}"
    else:
        return None, "❌ Incorrect password"


def create_otp_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_store (
        user_id INTEGER,
        otp TEXT,
        receiver TEXT,
        amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_otp(user_id, otp, receiver, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM otp_store WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
    INSERT INTO otp_store (user_id, otp, receiver, amount)
    VALUES (?, ?, ?, ?)
    """, (user_id, otp, receiver, amount))

    conn.commit()
    conn.close()


def get_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT otp, receiver, amount
    FROM otp_store
    WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()
    return row


def delete_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM otp_store WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def get_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT balance
    FROM accounts
    WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0


def make_transfer(user_id, receiver_name, amount):
    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Current balance
    cursor.execute("""
    SELECT balance FROM accounts WHERE user_id = ?
    """, (user_id,))
    balance = cursor.fetchone()[0]

    if balance < amount:
        conn.close()
        return False, "❌ Insufficient balance"

    # 2️⃣ Update balance
    cursor.execute("""
    UPDATE accounts
    SET balance = balance - ?
    WHERE user_id = ?
    """, (amount, user_id))

    # 3️⃣ Insert transaction
    cursor.execute("""
    INSERT INTO transactions (user_id, amount, transaction_type, description)
    VALUES (?, ?, 'debit', ?)
    """, (user_id, -amount, receiver_name))

    conn.commit()
    conn.close()

    return True, f"✅ ₹{amount} sent to {receiver_name}"


