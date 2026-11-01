import sqlite3
import os


# ==========================================
# DATABASE PATH
# ==========================================

DATABASE_PATH = "database/expense_tracker.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DATABASE_PATH)


# ==========================================
# CREATE ALL TABLES
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ======================================
    # USERS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ======================================
    # EXPENSES TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    # ======================================
    # CATEGORIES TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    # ======================================
    # BUDGETS TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            budget_amount REAL NOT NULL,

            UNIQUE(user_id, month, year),

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)
        # ======================================
    # INCOME TABLE
    # ======================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            description TEXT,
            income_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# RUN DATABASE FILE DIRECTLY
# ==========================================

if __name__ == "__main__":

    create_tables()

    print("Database and tables created successfully!")
