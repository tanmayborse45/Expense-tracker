import sqlite3
from datetime import datetime

from database import get_connection


# ==========================================
# CREATE BUDGET TABLE
# ==========================================

def create_budget_table():

    conn = get_connection()
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()


# ==========================================
# SET / UPDATE BUDGET
# ==========================================

def set_budget(user_id):

    print("\n==============================")
    print("     SET / UPDATE BUDGET")
    print("==============================")

    try:

        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year: "))
        amount = float(input("Enter monthly budget: "))

        if month < 1 or month > 12:
            print("\nInvalid month.")
            return

        if year < 2000:
            print("\nInvalid year.")
            return

        if amount <= 0:
            print("\nBudget must be greater than 0.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Check existing budget
        cursor.execute("""
            SELECT id
            FROM budgets
            WHERE user_id = ?
            AND month = ?
            AND year = ?
        """, (user_id, month, year))

        existing_budget = cursor.fetchone()

        if existing_budget:

            cursor.execute("""
                UPDATE budgets
                SET budget_amount = ?
                WHERE user_id = ?
                AND month = ?
                AND year = ?
            """, (
                amount,
                user_id,
                month,
                year
            ))

            print("\nBudget updated successfully.")

        else:

            cursor.execute("""
                INSERT INTO budgets
                (
                    user_id,
                    month,
                    year,
                    budget_amount
                )
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                month,
                year,
                amount
            ))

            print("\nBudget set successfully.")

        conn.commit()
        conn.close()

    except ValueError:

        print("\nPlease enter valid values.")

    except sqlite3.Error as e:

        print("\nDatabase error:", e)


# ==========================================
# VIEW BUDGET
# ==========================================

def view_budget(user_id):

    print("\n==============================")
    print("        VIEW BUDGET")
    print("==============================")

    try:

        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year: "))

        if month < 1 or month > 12:

            print("\nInvalid month.")
            return

        if year < 2000:

            print("\nInvalid year.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT budget_amount
            FROM budgets
            WHERE user_id = ?
            AND month = ?
            AND year = ?
        """, (
            user_id,
            month,
            year
        ))

        result = cursor.fetchone()

        conn.close()

        if result:

            budget_amount = result[0]

            month_name = datetime(
                year,
                month,
                1
            ).strftime("%B")

            print("\n------------------------------")
            print(f"Month       : {month_name} {year}")
            print(f"Budget      : ₹{budget_amount:.2f}")
            print("------------------------------")

        else:

            print("\nNo budget found for this month.")

    except ValueError:

        print("\nPlease enter valid values.")

    except sqlite3.Error as e:

        print("\nDatabase error:", e)


# ==========================================
# BUDGET VS EXPENSE
# ==========================================

def budget_vs_expense(user_id):

    print("\n==============================")
    print("      BUDGET VS EXPENSE")
    print("==============================")

    try:

        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year: "))

        if month < 1 or month > 12:

            print("\nInvalid month.")
            return

        if year < 2000:

            print("\nInvalid year.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # ----------------------------------
        # GET BUDGET
        # ----------------------------------

        cursor.execute("""
            SELECT budget_amount
            FROM budgets
            WHERE user_id = ?
            AND month = ?
            AND year = ?
        """, (
            user_id,
            month,
            year
        ))

        budget_result = cursor.fetchone()

        if not budget_result:

            print("\nNo budget found for this month.")

            conn.close()
            return

        budget_amount = budget_result[0]

        # ----------------------------------
        # GET MONTHLY EXPENSE
        # ----------------------------------

        # Example:
        # year  = 2026
        # month = 5
        #
        # month_text = "2026-05"
        #
        # It will find:
        # 2026-05-01
        # 2026-05-10
        # 2026-05-25
        # etc.

        month_text = f"{year}-{month:02d}"

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM expenses
            WHERE user_id = ?
            AND expense_date LIKE ?
        """, (
            user_id,
            f"{month_text}%"
        ))

        expense_result = cursor.fetchone()

        total_expense = expense_result[0]

        conn.close()

        # ----------------------------------
        # CALCULATIONS
        # ----------------------------------

        remaining = budget_amount - total_expense

        if budget_amount > 0:

            used_percentage = (
                total_expense / budget_amount
            ) * 100

        else:

            used_percentage = 0

        month_name = datetime(
            year,
            month,
            1
        ).strftime("%B")

        # ----------------------------------
        # DISPLAY RESULT
        # ----------------------------------

        print("\n==============================")
        print("      BUDGET VS EXPENSE")
        print("==============================")

        print(f"Month          : {month_name} {year}")
        print(f"Budget         : ₹{budget_amount:.2f}")
        print(f"Total Expense  : ₹{total_expense:.2f}")

        if remaining >= 0:

            print(f"Remaining      : ₹{remaining:.2f}")

        else:

            print(f"Exceeded       : ₹{abs(remaining):.2f}")

        print(f"Used           : {used_percentage:.2f}%")

        print("------------------------------")

        if total_expense <= budget_amount:

            print("Status         : Within Budget")

        else:

            print("Status         : Budget Exceeded")

        print("==============================")


    except ValueError:

        print("\nPlease enter valid values.")

    except sqlite3.Error as e:

        print("\nDatabase error:", e)


# ==========================================
# BUDGET MENU
# ==========================================

def budget_menu(user_id):

    create_budget_table()

    while True:

        print("\n==============================")
        print("       MONTHLY BUDGET")
        print("==============================")

        print("1. Set / Update Budget")
        print("2. View Budget")
        print("3. Budget vs Expense")
        print("4. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            set_budget(user_id)

        elif choice == "2":

            view_budget(user_id)

        elif choice == "3":

            budget_vs_expense(user_id)

        elif choice == "4":

            break

        else:

            print("\nInvalid choice. Please try again.")
