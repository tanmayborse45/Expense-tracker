from database import get_connection
from datetime import datetime


# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(user_id):

    print("\n==============================")
    print("         ADD EXPENSE")
    print("==============================")

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    description = input("Enter description: ").strip()

    expense_date = input(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    ).strip()

    # Agar date nahi di toh today's date
    if not expense_date:
        expense_date = datetime.now().strftime("%Y-%m-%d")

    # Date validate karna
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        print("Please use YYYY-MM-DD.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (
            user_id,
            amount,
            category,
            description,
            expense_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        amount,
        category,
        description,
        expense_date
    ))

    conn.commit()
    conn.close()

    print("\nExpense added successfully!")


# ==========================================
# VIEW EXPENSES
# ==========================================

def view_expenses(user_id):

    print("\n================================================")
    print("                 YOUR EXPENSES")
    print("================================================")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            amount,
            category,
            description,
            expense_date
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC, id DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    conn.close()

    if not expenses:
        print("No expenses found.")
        return

    print(
        f"{'ID':<5}"
        f"{'Amount':<12}"
        f"{'Category':<18}"
        f"{'Description':<25}"
        f"{'Date':<12}"
    )

    print("-" * 72)

    for expense in expenses:

        expense_id = expense[0]
        amount = expense[1]
        category = expense[2]
        description = expense[3] or ""
        expense_date = expense[4]

        print(
            f"{expense_id:<5}"
            f"₹{amount:<11.2f}"
            f"{category:<18}"
            f"{description:<25}"
            f"{expense_date:<12}"
        )


# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(user_id):

    print("\n==============================")
    print("        UPDATE EXPENSE")
    print("==============================")

    view_expenses(user_id)

    try:
        expense_id = int(
            input("\nEnter Expense ID to update: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    # Check expense belongs to this user
    cursor.execute("""
        SELECT id
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id, user_id))

    expense = cursor.fetchone()

    if not expense:
        print("Expense not found.")
        conn.close()
        return

    print("\nLeave field empty to keep old value.")

    amount_input = input("New amount: ").strip()
    category = input("New category: ").strip()
    description = input("New description: ").strip()
    expense_date = input(
        "New date (YYYY-MM-DD): "
    ).strip()

    # Current data
    cursor.execute("""
        SELECT amount, category, description, expense_date
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id, user_id))

    old_data = cursor.fetchone()

    old_amount = old_data[0]
    old_category = old_data[1]
    old_description = old_data[2]
    old_date = old_data[3]

    # Amount
    if amount_input:
        try:
            amount = float(amount_input)

            if amount <= 0:
                print("Amount must be greater than 0.")
                conn.close()
                return

        except ValueError:
            print("Invalid amount.")
            conn.close()
            return
    else:
        amount = old_amount

    # Category
    if not category:
        category = old_category

    # Description
    if not description:
        description = old_description

    # Date
    if not expense_date:
        expense_date = old_date
    else:
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date.")
            conn.close()
            return

    cursor.execute("""
        UPDATE expenses
        SET
            amount = ?,
            category = ?,
            description = ?,
            expense_date = ?
        WHERE id = ?
        AND user_id = ?
    """, (
        amount,
        category,
        description,
        expense_date,
        expense_id,
        user_id
    ))

    conn.commit()
    conn.close()

    print("\nExpense updated successfully!")


# ==========================================
# DELETE EXPENSE
# ==========================================

def delete_expense(user_id):

    print("\n==============================")
    print("        DELETE EXPENSE")
    print("==============================")

    view_expenses(user_id)

    try:
        expense_id = int(
            input("\nEnter Expense ID to delete: ")
        )
    except ValueError:
        print("Invalid ID.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM expenses
        WHERE id = ?
        AND user_id = ?
    """, (expense_id, user_id))

    expense = cursor.fetchone()

    if not expense:
        print("Expense not found.")
        conn.close()
        return

    confirm = input(
        "Are you sure you want to delete this expense? (y/n): "
    ).lower()

    if confirm == "y":

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ?
            AND user_id = ?
        """, (expense_id, user_id))

        conn.commit()

        print("Expense deleted successfully!")

    else:

        print("Delete cancelled.")

    conn.close()
