from database import get_connection


# ==========================================
# SEARCH EXPENSE
# ==========================================

def search_expense(user_id):

    print("\n==============================")
    print("       SEARCH EXPENSE")
    print("==============================")

    keyword = input(
        "Enter category or description: "
    ).strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE user_id = ?
        AND (
            category LIKE ?
            OR description LIKE ?
        )
        ORDER BY expense_date DESC
    """, (
        user_id,
        f"%{keyword}%",
        f"%{keyword}%"
    ))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("\nNo matching expenses found.")
        return

    print("\nID   Amount      Category          Description          Date")
    print("-" * 70)

    for expense in expenses:
        print(
            f"{expense[0]:<5}"
            f"₹{expense[1]:<11.2f}"
            f"{expense[2]:<18}"
            f"{(expense[3] or ''):<21}"
            f"{expense[4]:<12}"
        )


# ==========================================
# FILTER BY CATEGORY
# ==========================================

def filter_by_category(user_id):

    print("\n==============================")
    print("     FILTER BY CATEGORY")
    print("==============================")

    category = input("Enter category: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE user_id = ?
        AND category LIKE ?
        ORDER BY expense_date DESC
    """, (
        user_id,
        f"%{category}%"
    ))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("\nNo expenses found.")
        return

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


# ==========================================
# FILTER BY DATE
# ==========================================

def filter_by_date(user_id):

    print("\n==============================")
    print("        FILTER BY DATE")
    print("==============================")

    date = input("Enter date (YYYY-MM-DD): ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE user_id = ?
        AND expense_date = ?
        ORDER BY id DESC
    """, (user_id, date))

    expenses = cursor.fetchall()
    conn.close()

    if not expenses:
        print("\nNo expenses found.")
        return

    for expense in expenses:
        print(
            f"ID: {expense[0]} | "
            f"Amount: ₹{expense[1]:.2f} | "
            f"Category: {expense[2]} | "
            f"Description: {expense[3]} | "
            f"Date: {expense[4]}"
        )


# ==========================================
# MONTHLY REPORT
# ==========================================

def monthly_report(user_id):

    print("\n==============================")
    print("        MONTHLY REPORT")
    print("==============================")

    month = input("Enter month (YYYY-MM): ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', expense_date) = ?
    """, (user_id, month))

    result = cursor.fetchone()
    conn.close()

    print("\n------------------------------")
    print(f"Month: {month}")
    print(f"Number of Expenses: {result[0]}")
    print(f"Total Spending: ₹{result[1]:.2f}")
    print("------------------------------")


# ==========================================
# CATEGORY-WISE REPORT
# ==========================================

def category_report(user_id):

    print("\n==============================")
    print("     CATEGORY-WISE REPORT")
    print("==============================")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, COUNT(*), SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (user_id,))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print("\nNo expenses found.")
        return

    print("\nCategory          Count       Total")
    print("------------------------------------------")

    for category, count, total in results:
        print(
            f"{category:<18}"
            f"{count:<12}"
            f"₹{total:.2f}"
        )


# ==========================================
# REPORT MENU
# ==========================================

def reports_menu(user_id):

    while True:

        print("\n================================")
        print("            REPORTS")
        print("================================")

        print("1. Search Expense")
        print("2. Filter by Category")
        print("3. Filter by Date")
        print("4. Monthly Report")
        print("5. Category-wise Report")
        print("6. Back")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            search_expense(user_id)

        elif choice == "2":
            filter_by_category(user_id)

        elif choice == "3":
            filter_by_date(user_id)

        elif choice == "4":
            monthly_report(user_id)

        elif choice == "5":
            category_report(user_id)

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")
