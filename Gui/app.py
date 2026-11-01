import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from auth import register_user, login_user
from database import get_connection

# ==========================================
# REGISTER WINDOW
# ==========================================
# ==========================================
# DASHBOARD WINDOW
# ==========================================
# ==========================================
# ADD EXPENSE WINDOW
# ==========================================

def open_add_expense_window(user_id):

    expense_window = tk.Toplevel(root)

    expense_window.title("Add Expense")
    expense_window.geometry("400x450")

    # Heading
    title_label = tk.Label(
        expense_window,
        text="ADD EXPENSE",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    # -------------------------
    # Amount
    # -------------------------

    amount_label = tk.Label(
        expense_window,
        text="Amount"
    )

    amount_label.pack()

    amount_entry = tk.Entry(
        expense_window,
        width=30
    )

    amount_entry.pack(pady=5)

    # -------------------------
    # Category
    # -------------------------

    category_label = tk.Label(
        expense_window,
        text="Category"
    )

    category_label.pack()

    category_entry = tk.Entry(
        expense_window,
        width=30
    )

    category_entry.pack(pady=5)

    # -------------------------
    # Description
    # -------------------------

    description_label = tk.Label(
        expense_window,
        text="Description"
    )

    description_label.pack()

    description_entry = tk.Entry(
        expense_window,
        width=30
    )

    description_entry.pack(pady=5)

    # -------------------------
    # Date
    # -------------------------

    date_label = tk.Label(
        expense_window,
        text="Date (YYYY-MM-DD)"
    )

    date_label.pack()

    date_entry = tk.Entry(
        expense_window,
        width=30
    )

    date_entry.pack(pady=5)

    # -------------------------
    # ADD EXPENSE FUNCTION
    # -------------------------

    
    def add_expense_gui():
        amount_text = amount_entry.get().strip()
        category = category_entry.get().strip()
        description = description_entry.get().strip()
        expense_date = date_entry.get().strip()

        # Validate required fields
        if not amount_text or not category or not expense_date:
            messagebox.showwarning(
                "Warning",
                "Please fill all required fields."
            )
            return

        # Validate amount
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        if amount <= 0:
            messagebox.showwarning(
                "Warning",
                "Amount must be greater than 0."
            )
            return

        # Validate date
        from datetime import datetime

        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error",
                "Date must be in YYYY-MM-DD format."
            )
            return

        # Save only after all validations pass
        conn = get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO expenses
                (user_id, amount, category, description, expense_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    amount,
                    category,
                    description,
                    expense_date
                )
            )
            conn.commit()

        except Exception as error:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                str(error)
            )
            return

        finally:
            conn.close()

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )
        expense_window.destroy()
        
    add_button = tk.Button(
        expense_window,
        text="ADD EXPENSE",
        width=20,
        command=add_expense_gui
    )
    add_button.pack(pady=20)

    back_button = tk.Button(
        expense_window,
        text="BACK",
        width=20,
        command=expense_window.destroy
    )
    back_button.pack()

def open_add_income_window(user_id):
    from datetime import datetime

    income_window = tk.Toplevel(root)
    income_window.title("Add Income")
    income_window.geometry("400x450")

    tk.Label(
        income_window,
        text="ADD INCOME",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(income_window, text="Amount").pack()
    amount_entry = tk.Entry(income_window)
    amount_entry.pack(pady=5)

    tk.Label(income_window, text="Income Source").pack()
    source_entry = tk.Entry(income_window)
    source_entry.pack(pady=5)

    tk.Label(income_window, text="Description").pack()
    description_entry = tk.Entry(income_window)
    description_entry.pack(pady=5)

    tk.Label(income_window, text="Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(income_window)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    date_entry.pack(pady=5)

    def save_income():
        try:
            amount = float(amount_entry.get())

            if amount <= 0:
                messagebox.showerror(
                    "Error", "Amount must be greater than 0"
                )
                return

            source = source_entry.get().strip()
            description = description_entry.get().strip()
            income_date = date_entry.get().strip()

            if not source:
                messagebox.showerror("Error", "Please enter income source")
                return

            datetime.strptime(income_date, "%Y-%m-%d")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO income
                (user_id, amount, source, description, income_date)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, amount, source, description, income_date))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Income added successfully!")
            income_window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid amount and date (YYYY-MM-DD)"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(
        income_window,
        text="SAVE INCOME",
        command=save_income,
        bg="green",
        fg="white"
    ).pack(pady=20)

def open_view_income_window(user_id):

    income_window = tk.Toplevel(root)
    income_window.title("View Income")
    income_window.geometry("850x550")

    tk.Label(
        income_window,
        text="INCOME DETAILS",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    # Total Income
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM income
        WHERE user_id = ?
    """, (user_id,))

    total_income = cursor.fetchone()[0]

    conn.close()

    tk.Label(
        income_window,
        text=f"TOTAL INCOME: ₹{total_income:.2f}",
        font=("Arial", 14, "bold"),
        fg="green"
    ).pack(pady=10)

    # Income Table
    columns = ("ID", "Amount", "Source", "Description", "Date")

    income_table = ttk.Treeview(
        income_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        income_table.heading(column, text=column)
        income_table.column(column, width=150)

    income_table.pack(fill="both", expand=True, padx=15, pady=15)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, source, description, income_date
        FROM income
        WHERE user_id = ?
        ORDER BY income_date DESC
    """, (user_id,))

    records = cursor.fetchall()

    for record in records:
        income_table.insert("", "end", values=record)

    conn.close()

def open_savings_window(user_id):

    savings_window = tk.Toplevel(root)
    savings_window.title("Savings Calculator")
    savings_window.geometry("450x400")

    tk.Label(
        savings_window,
        text="SAVINGS SUMMARY",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM income
        WHERE user_id = ?
    """, (user_id,))

    total_income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    total_expenses = cursor.fetchone()[0]

    conn.close()

    savings = total_income - total_expenses

    tk.Label(
        savings_window,
        text=f"Total Income: ₹{total_income:.2f}",
        font=("Arial", 13)
    ).pack(pady=10)

    tk.Label(
        savings_window,
        text=f"Total Expenses: ₹{total_expenses:.2f}",
        font=("Arial", 13)
    ).pack(pady=10)

    tk.Label(
        savings_window,
        text=f"Total Savings: ₹{savings:.2f}",
        font=("Arial", 16, "bold"),
        fg="green" if savings >= 0 else "red"
    ).pack(pady=20)    


def open_monthly_comparison_window(user_id):

    from datetime import date, timedelta

    comparison_window = tk.Toplevel(root)
    comparison_window.title("Monthly Expense Comparison")
    comparison_window.geometry("500x450")

    tk.Label(
        comparison_window,
        text="MONTHLY COMPARISON",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    # Current and Previous Month
    today = date.today()
    current_month_start = today.replace(day=1)

    previous_month_last_day = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_last_day.replace(day=1)

    next_month_start = (
        current_month_start.replace(day=28) + timedelta(days=4)
    ).replace(day=1)

    current_start = current_month_start.strftime("%Y-%m-%d")
    current_end = next_month_start.strftime("%Y-%m-%d")

    previous_start = previous_month_start.strftime("%Y-%m-%d")
    previous_end = current_start

    conn = get_connection()
    cursor = conn.cursor()

    # Previous Month Expenses
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND expense_date >= ?
        AND expense_date < ?
    """, (user_id, previous_start, previous_end))

    previous_expenses = cursor.fetchone()[0]

    # Current Month Expenses
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND expense_date >= ?
        AND expense_date < ?
    """, (user_id, current_start, current_end))

    current_expenses = cursor.fetchone()[0]

    conn.close()

    difference = current_expenses - previous_expenses

    # Display Results
    tk.Label(
        comparison_window,
        text=f"Previous Month Expenses: ₹{previous_expenses:.2f}",
        font=("Arial", 13)
    ).pack(pady=15)

    tk.Label(
        comparison_window,
        text=f"Current Month Expenses: ₹{current_expenses:.2f}",
        font=("Arial", 13)
    ).pack(pady=15)

    tk.Label(
        comparison_window,
        text=f"Difference: ₹{abs(difference):.2f}",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    if difference > 0:
        result = "Your expenses increased this month."
        color = "red"
    elif difference < 0:
        result = "Your expenses decreased this month."
        color = "green"
    else:
        result = "Your expenses are unchanged."
        color = "blue"

    tk.Label(
        comparison_window,
        text=result,
        font=("Arial", 12, "bold"),
        fg=color,
        wraplength=400
    ).pack(pady=20)

def export_expenses_to_excel(user_id):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, expense_date
            FROM expenses
            WHERE user_id = ?
            ORDER BY expense_date DESC
        """, (user_id,))

        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo(
                "No Data",
                "No expenses available to export."
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Expense Report",
            initialfile="Expense_Report.xlsx"
        )

        if not file_path:
            return

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Expenses"

        sheet.append([
            "Expense ID",
            "Amount",
            "Category",
            "Description",
            "Date"
        ])

        for record in records:
            sheet.append(list(record))

        # Adjust column widths
        for column in sheet.columns:
            max_length = max(
                len(str(cell.value or "")) for cell in column
            )
            sheet.column_dimensions[
                column[0].column_letter
            ].width = max_length + 3

        workbook.save(file_path)

        messagebox.showinfo(
            "Success",
            "Expenses exported successfully to Excel!"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def export_expenses_to_pdf(user_id):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, amount, category, description, expense_date
            FROM expenses
            WHERE user_id = ?
            ORDER BY expense_date DESC
        """, (user_id,))

        records = cursor.fetchall()
        conn.close()

        if not records:
            messagebox.showinfo(
                "No Data",
                "No expenses available to export."
            )
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Expense Report",
            initialfile="Expense_Report.pdf"
        )

        if not file_path:
            return

        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        y = height - 50

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(50, y, "EXPENSE REPORT")

        y -= 40

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, "ID")
        pdf.drawString(85, y, "Amount")
        pdf.drawString(160, y, "Category")
        pdf.drawString(260, y, "Description")
        pdf.drawString(430, y, "Date")

        y -= 20

        pdf.setFont("Helvetica", 9)

        for record in records:

            if y < 50:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 9)

            expense_id, amount, category, description, expense_date = record

            pdf.drawString(50, y, str(expense_id))
            pdf.drawString(85, y, str(amount))
            pdf.drawString(160, y, str(category)[:15])
            pdf.drawString(260, y, str(description or "")[:25])
            pdf.drawString(430, y, str(expense_date))

            y -= 20

        pdf.save()

        messagebox.showinfo(
            "Success",
            "Expenses exported successfully to PDF!"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ==========================================
# VIEW EXPENSES WINDOW
# ==========================================

def open_view_expenses_window(user_id):

    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")
    view_window.geometry("900x550")

    # Heading
    title_label = tk.Label(
        view_window,
        text="YOUR EXPENSES",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=20)

    # Filter frame
    filter_frame = tk.Frame(view_window)
    filter_frame.pack(pady=10)

    # Category
    category_label = tk.Label(
        filter_frame,
        text="Category:"
    )
    category_label.grid(row=0, column=0, padx=5)

    category_entry = tk.Entry(
        filter_frame,
        width=20
    )
    category_entry.grid(row=0, column=1, padx=5)

    # Date
    date_label = tk.Label(
        filter_frame,
        text="Date:"
    )
    date_label.grid(row=0, column=2, padx=5)

    date_entry = tk.Entry(
        filter_frame,
        width=15
    )
    date_entry.grid(row=0, column=3, padx=5)

    # Table frame
    table_frame = tk.Frame(view_window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # Table columns
    columns = (
        "ID",
        "Amount",
        "Category",
        "Description",
        "Date"
    )

    expense_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    expense_table.heading("ID", text="ID")
    expense_table.heading("Amount", text="Amount")
    expense_table.heading("Category", text="Category")
    expense_table.heading("Description", text="Description")
    expense_table.heading("Date", text="Date")

    expense_table.column("ID", width=50)
    expense_table.column("Amount", width=100)
    expense_table.column("Category", width=150)
    expense_table.column("Description", width=300)
    expense_table.column("Date", width=120)

    expense_table.pack(
        fill="both",
        expand=True
    )

    # Function to display expenses
    def display_expenses(expenses):

        # Existing table records remove
        for item in expense_table.get_children():
            expense_table.delete(item)

        # New records add
        for expense in expenses:

            expense_table.insert(
                "",
                "end",
                values=(
                    expense[0],
                    f"₹{expense[1]:.2f}",
                    expense[2],
                    expense[3] or "",
                    expense[4]
                )
            )

    # Search / Filter function
    def search_filter_expenses():

        category = category_entry.get().strip()
        expense_date = date_entry.get().strip()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                id,
                amount,
                category,
                description,
                expense_date
            FROM expenses
            WHERE user_id = ?
        """

        params = [user_id]

        # Category filter
        if category:
            query += " AND category LIKE ?"
            params.append("%" + category + "%")

        # Date filter
        if expense_date:
            query += " AND expense_date = ?"
            params.append(expense_date)

        query += " ORDER BY expense_date DESC, id DESC"

        cursor.execute(query, params)

        expenses = cursor.fetchall()

        conn.close()

        display_expenses(expenses)

        if not expenses:
            messagebox.showinfo(
                "Search Result",
                "No matching expenses found."
            )

    # Show all expenses function
    def show_all_expenses():

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

        display_expenses(expenses)

    # Search button
    search_button = tk.Button(
        filter_frame,
        text="SEARCH / FILTER",
        width=18,
        command=search_filter_expenses
    )
    search_button.grid(
        row=0,
        column=4,
        padx=5
    )

    # Show all button
    show_all_button = tk.Button(
        filter_frame,
        text="SHOW ALL",
        width=12,
        command=show_all_expenses
    )
    show_all_button.grid(
        row=0,
        column=5,
        padx=5
    )

    # Initially show all expenses
    show_all_expenses()

    # Back button
    back_button = tk.Button(
        view_window,
        text="BACK",
        width=20,
        command=view_window.destroy
    )

    back_button.pack(pady=15)
# ==========================================
# UPDATE EXPENSE WINDOW
# ==========================================

def open_update_expense_window(user_id):

    update_window = tk.Toplevel(root)

    update_window.title("Update Expense")
    update_window.geometry("850x650")

    # ==========================================
    # HEADING
    # ==========================================

    title_label = tk.Label(
        update_window,
        text="UPDATE EXPENSE",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=15)

    # ==========================================
    # TABLE
    # ==========================================

    table_frame = tk.Frame(update_window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "ID",
        "Amount",
        "Category",
        "Description",
        "Date"
    )

    expense_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    expense_table.heading(
        "ID",
        text="ID"
    )

    expense_table.heading(
        "Amount",
        text="Amount"
    )

    expense_table.heading(
        "Category",
        text="Category"
    )

    expense_table.heading(
        "Description",
        text="Description"
    )

    expense_table.heading(
        "Date",
        text="Date"
    )

    expense_table.column(
        "ID",
        width=50
    )

    expense_table.column(
        "Amount",
        width=100
    )

    expense_table.column(
        "Category",
        width=150
    )

    expense_table.column(
        "Description",
        width=250
    )

    expense_table.column(
        "Date",
        width=120
    )

    expense_table.pack(
        fill="both",
        expand=True
    )

    # ==========================================
    # GET USER EXPENSES
    # ==========================================

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

    # ==========================================
    # DISPLAY EXPENSES
    # ==========================================

    for expense in expenses:

        expense_table.insert(
            "",
            "end",
            values=(
                expense[0],
                f"₹{expense[1]:.2f}",
                expense[2],
                expense[3] or "",
                expense[4]
            )
        )

    # ==========================================
    # UPDATE FORM
    # ==========================================

    form_frame = tk.Frame(update_window)

    form_frame.pack(
        pady=10
    )

    # Amount
    amount_label = tk.Label(
        form_frame,
        text="Amount"
    )

    amount_label.grid(
        row=0,
        column=0,
        padx=10,
        pady=5
    )

    amount_entry = tk.Entry(
        form_frame,
        width=25
    )

    amount_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=5
    )

    # Category
    category_label = tk.Label(
        form_frame,
        text="Category"
    )

    category_label.grid(
        row=1,
        column=0,
        padx=10,
        pady=5
    )

    category_entry = tk.Entry(
        form_frame,
        width=25
    )

    category_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=5
    )

    # Description
    description_label = tk.Label(
        form_frame,
        text="Description"
    )

    description_label.grid(
        row=2,
        column=0,
        padx=10,
        pady=5
    )

    description_entry = tk.Entry(
        form_frame,
        width=25
    )

    description_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=5
    )

    # Date
    date_label = tk.Label(
        form_frame,
        text="Date (YYYY-MM-DD)"
    )

    date_label.grid(
        row=3,
        column=0,
        padx=10,
        pady=5
    )

    date_entry = tk.Entry(
        form_frame,
        width=25
    )

    date_entry.grid(
        row=3,
        column=1,
        padx=10,
        pady=5
    )

    # ==========================================
    # SELECT EXPENSE FUNCTION
    # ==========================================
    
    def select_expense():

        selected_item = expense_table.selection()

        if not selected_item:

            messagebox.showwarning(
                "Warning",
                "Please select an expense first."
            )

            return

        selected_values = expense_table.item(
            selected_item[0],
            "values"
        )

        expense_id = selected_values[0]

        amount = selected_values[1]

        category = selected_values[2]

        description = selected_values[3]

        expense_date = selected_values[4]

        # Clear old values
        amount_entry.delete(
            0,
            tk.END
        )

        category_entry.delete(
            0,
            tk.END
        )

        description_entry.delete(
            0,
            tk.END
        )

        date_entry.delete(
            0,
            tk.END
        )

        # Insert selected values
        amount_entry.insert(
            0,
            amount.replace("₹", "")
        )

        category_entry.insert(
            0,
            category
        )

        description_entry.insert(
            0,
            description
        )

        date_entry.insert(
            0,
            expense_date
        )

        # Store selected expense ID
        update_window.selected_expense_id = expense_id

    # ==========================================
    # SELECT BUTTON
    # ==========================================

    select_button = tk.Button(
        update_window,
        text="SELECT EXPENSE",
        width=20,
        command=select_expense
    )

    select_button.pack(
        pady=5
    )

    # ==========================================
    # UPDATE EXPENSE FUNCTION
    # ==========================================

    def update_expense():

        if not hasattr(
            update_window,
            "selected_expense_id"
        ):

            messagebox.showwarning(
                "Warning",
                "Please select an expense first."
            )

            return

        amount = amount_entry.get().strip()

        category = category_entry.get().strip()

        description = description_entry.get().strip()

        expense_date = date_entry.get().strip()

        # Check required fields
        if not amount or not category or not expense_date:

            messagebox.showwarning(
                "Warning",
                "Please fill all required fields."
            )

            return

        # Validate amount
        try:

            amount = float(amount)

            if amount <= 0:

                messagebox.showwarning(
                    "Warning",
                    "Amount must be greater than 0."
                )

                return

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )

            return

        # Validate date
        from datetime import datetime

        try:

            datetime.strptime(
                expense_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Date must be in YYYY-MM-DD format."
            )

            return

        # ==========================================
        # UPDATE DATABASE
        # ==========================================

        conn = get_connection()

        cursor = conn.cursor()

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
            update_window.selected_expense_id,
            user_id
        ))

        conn.commit()

        conn.close()

        # Success message
        messagebox.showinfo(
            "Success",
            "Expense updated successfully!"
        )

        # Close window
        update_window.destroy()

    # ==========================================
    # UPDATE BUTTON
    # ==========================================

    update_button = tk.Button(
        update_window,
        text="UPDATE EXPENSE",
        width=20,
        command=update_expense
    )

    update_button.pack(
        pady=5
    )

    # ==========================================
    # BACK BUTTON
    # ==========================================

    back_button = tk.Button(
        update_window,
        text="BACK",
        width=20,
        command=update_window.destroy
    )

    back_button.pack(
        pady=10
    )
def open_delete_expense_window(user_id):

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Expense")
    delete_window.geometry("850x550")

    title_label = tk.Label(
        delete_window,
        text="DELETE EXPENSE",
        font=("Arial", 20, "bold")
    )
    title_label.pack(pady=15)

    table_frame = tk.Frame(delete_window)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Amount", "Category", "Description", "Date")

    expense_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    expense_table.heading("ID", text="ID")
    expense_table.heading("Amount", text="Amount")
    expense_table.heading("Category", text="Category")
    expense_table.heading("Description", text="Description")
    expense_table.heading("Date", text="Date")

    expense_table.column("ID", width=50)
    expense_table.column("Amount", width=100)
    expense_table.column("Category", width=150)
    expense_table.column("Description", width=250)
    expense_table.column("Date", width=120)

    expense_table.pack(fill="both", expand=True)

    # Database se expenses fetch karna
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC, id DESC
    """, (user_id,))

    expenses = cursor.fetchall()

    conn.close()

    # Table mein expenses show karna
    for expense in expenses:
        expense_table.insert(
            "",
            "end",
            values=(
                expense[0],
                f"₹{expense[1]:.2f}",
                expense[2],
                expense[3] or "",
                expense[4]
            )
        )

    def delete_expense():

        selected_item = expense_table.selection()

        if not selected_item:
            messagebox.showwarning(
                "Warning",
                "Please select an expense first."
            )
            return

        selected_values = expense_table.item(
            selected_item[0],
            "values"
        )

        expense_id = selected_values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        )

        if not confirm:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM expenses
            WHERE id = ? AND user_id = ?
        """, (expense_id, user_id))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Expense deleted successfully!"
        )

        delete_window.destroy()

    delete_button = tk.Button(
        delete_window,
        text="DELETE SELECTED EXPENSE",
        width=25,
        command=delete_expense
    )
    delete_button.pack(pady=10)

    back_button = tk.Button(
        delete_window,
        text="BACK",
        width=20,
        command=delete_window.destroy
    )
    back_button.pack(pady=10)
def open_reports_window(user_id):
    reports_window = tk.Toplevel(root)
    reports_window.title("Expense Reports")
    reports_window.geometry("500x700")

    # Main Canvas
    canvas = tk.Canvas(reports_window)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(
        reports_window,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable Frame
    scrollable_frame = tk.Frame(canvas)

    canvas_window = canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    # Update scroll area
    def update_scrollregion(event):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    scrollable_frame.bind(
        "<Configure>",
        update_scrollregion
    )

    # Make frame same width as window
    def resize_frame(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    canvas.bind("<Configure>", resize_frame)

    # Title
    title_label = tk.Label(
        scrollable_frame,
        text="EXPENSE REPORT",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=20)

    # Total Expenses
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    total_expenses = result[0]
    total_amount = result[1]

    count_label = tk.Label(
        scrollable_frame,
        text=f"Total Expenses: {total_expenses}",
        font=("Arial", 14)
    )
    count_label.pack(pady=10)

    amount_label = tk.Label(
        scrollable_frame,
        text=f"Total Amount: ₹{total_amount:.2f}",
        font=("Arial", 14)
    )
    amount_label.pack(pady=10)

    # Category Wise Expenses
    category_label = tk.Label(
        scrollable_frame,
        text="CATEGORY-WISE EXPENSES",
        font=("Arial", 14, "bold")
    )
    category_label.pack(pady=15)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (user_id,))

    category_expenses = cursor.fetchall()
    conn.close()

    for category, amount in category_expenses:
        category_item = tk.Label(
            scrollable_frame,
            text=f"{category}: ₹{amount:.2f}",
            font=("Arial", 12)
        )
        category_item.pack(pady=3)

    # Pie Chart
    if category_expenses:
        chart_canvas = tk.Canvas(
            scrollable_frame,
            width=300,
            height=250,
            bg="white"
        )
        chart_canvas.pack(pady=20)

        total = sum(
            amount for category, amount in category_expenses
        )

        colors = [
            "lightblue",
            "lightgreen",
            "lightcoral",
            "khaki",
            "plum",
            "orange",
            "lightpink",
            "lightgray"
        ]

        start_angle = 0

        for index, (category, amount) in enumerate(category_expenses):
            extent = (amount / total) * 360

            chart_canvas.create_arc(
                50,
                20,
                250,
                220,
                start=start_angle,
                extent=extent,
                fill=colors[index % len(colors)],
                outline="black"
            )

            start_angle += extent

    # Monthly Expenses
    month_label = tk.Label(
        scrollable_frame,
        text="MONTHLY EXPENSES",
        font=("Arial", 14, "bold")
    )
    month_label.pack(pady=15)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', expense_date), SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY strftime('%Y-%m', expense_date)
        ORDER BY strftime('%Y-%m', expense_date) DESC
    """, (user_id,))

    monthly_expenses = cursor.fetchall()
    conn.close()

    for month, amount in monthly_expenses:
        month_item = tk.Label(
            scrollable_frame,
            text=f"{month}: ₹{amount:.2f}",
            font=("Arial", 12)
        )
        month_item.pack(pady=3)

    # Refresh Button
    refresh_button = tk.Button(
        scrollable_frame,
        text="REFRESH REPORT",
        width=20,
        height=2,
        command=lambda: [
            reports_window.destroy(),
            open_reports_window(user_id)
        ]
    )
    refresh_button.pack(pady=15)

    # Close Button
    close_button = tk.Button(
        scrollable_frame,
        text="CLOSE",
        width=20,
        height=2,
        command=reports_window.destroy
    )
    close_button.pack(pady=20)

def open_budget_window(user_id):
    budget_window = tk.Toplevel(root)
    budget_window.title("Monthly Budget")
    budget_window.geometry("500x550")

    title_label = tk.Label(
        budget_window,
        text="MONTHLY BUDGET",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=20)

    month_label = tk.Label(
        budget_window,
        text="Month (1-12):",
        font=("Arial", 12)
    )
    month_label.pack(pady=5)

    month_entry = tk.Entry(
        budget_window,
        width=30
    )
    month_entry.pack(pady=5)

    year_label = tk.Label(
        budget_window,
        text="Year:",
        font=("Arial", 12)
    )
    year_label.pack(pady=5)

    year_entry = tk.Entry(
        budget_window,
        width=30
    )
    year_entry.pack(pady=5)

    amount_label = tk.Label(
        budget_window,
        text="Budget Amount:",
        font=("Arial", 12)
    )
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(
        budget_window,
        width=30
    )
    amount_entry.pack(pady=5)

    def set_budget():
        month = month_entry.get().strip()
        year = year_entry.get().strip()
        amount = amount_entry.get().strip()

        if not month or not year or not amount:
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        try:
            month = int(month)
            year = int(year)
            amount = float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Month, Year and Budget Amount must be valid."
            )
            return

        if month < 1 or month > 12:
            messagebox.showerror(
                "Error",
                "Month must be between 1 and 12."
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Budget amount must be greater than 0."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO budgets
            (user_id, month, year, budget_amount)
            VALUES (?, ?, ?, ?)
        """, (user_id, month, year, amount))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Monthly budget saved successfully!"
        )

    def view_budget():
        month = month_entry.get().strip()
        year = year_entry.get().strip()

        if not month or not year:
            messagebox.showerror(
                "Error",
                "Please enter Month and Year."
            )
            return

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Month and Year must be valid."
            )
            return

        if month < 1 or month > 12:
            messagebox.showerror(
                "Error",
                "Month must be between 1 and 12."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT budget_amount
            FROM budgets
            WHERE user_id = ? AND month = ? AND year = ?
        """, (user_id, month, year))

        result = cursor.fetchone()

        conn.close()

        if result:
            messagebox.showinfo(
                "Current Budget",
                f"Budget for {month}/{year}: ₹{result[0]:.2f}"
            )
        else:
            messagebox.showinfo(
                "Current Budget",
                "No budget found for this month and year."
            )

    view_budget_button = tk.Button(
        budget_window,
        text="VIEW BUDGET",
        width=20,
        height=2,
        command=view_budget
    )
    view_budget_button.pack(pady=10)

    def budget_vs_expense():
        month = month_entry.get().strip()
        year = year_entry.get().strip()

        if not month or not year:
            messagebox.showerror(
                "Error",
                "Please enter Month and Year."
            )
            return

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Month and Year must be valid."
            )
            return

        if month < 1 or month > 12:
            messagebox.showerror(
                "Error",
                "Month must be between 1 and 12."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT budget_amount
            FROM budgets
            WHERE user_id = ? AND month = ? AND year = ?
        """, (user_id, month, year))

        budget_result = cursor.fetchone()

        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = ?
            AND expense_date LIKE ?
        """, (
            user_id,
            f"{year}-{month:02d}%"
        ))

        expense_result = cursor.fetchone()

        conn.close()

        if not budget_result:
            messagebox.showinfo(
                "Budget vs Expense",
                "No budget found for this month and year."
            )
            return

        budget = float(budget_result[0])
        expense = float(expense_result[0] or 0)
        remaining = budget - expense

        if expense <= budget:
         status = "Within Budget"
        else:
         status = "Budget Exceede"

        messagebox.showinfo(
            "Budget vs Expense",
            f"Month: {month}/{year}\n\n"
            f"Budget: ₹{budget:.2f}\n"
            f"Total Expense: ₹{expense:.2f}\n"
            f"Remaining: ₹{remaining:.2f}"
            f"Status: {status}"
        )
        
    
    budget_button = tk.Button(
        budget_window,
        text="SET BUDGET",
        width=20,
        height=2,
        command=set_budget
    )
    budget_button.pack(pady=10)

    budget_vs_expense_button = tk.Button(
        budget_window,
        text="BUDGET VS EXPENSE",
        width=20,
        height=2,
        command=budget_vs_expense
    )
    budget_vs_expense_button.pack(pady=10)

    close_button = tk.Button(
        budget_window,
        text="CLOSE",
        width=20,
        height=2,
        command=budget_window.destroy
    )
    close_button.pack(pady=10)




def open_dashboard_charts_window(user_id):
    # NOTE: this function expects these to already exist in your main file:
    #   tk, ttk, messagebox, root, get_connection

    try:
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from datetime import datetime
    except ImportError:
        messagebox.showerror(
            "Missing Library",
            "Please install matplotlib first:\n\npip install matplotlib"
        )
        return

    # ---------- Window ----------
    chart_window = tk.Toplevel(root)
    chart_window.title("Expense Analytics")
    chart_window.geometry("1100x760")
    chart_window.configure(bg="#F1F5F9")

    tk.Label(
        chart_window,
        text="EXPENSE ANALYTICS DASHBOARD",
        font=("Arial", 21, "bold"),
        bg="#F1F5F9",
        fg="#1E293B"
    ).pack(pady=15)

    # ---------- Period filter ----------
    filter_frame = tk.Frame(chart_window, bg="#F1F5F9")
    filter_frame.pack(pady=5)

    tk.Label(
        filter_frame,
        text="SELECT PERIOD:",
        font=("Arial", 10, "bold"),
        bg="#F1F5F9",
        fg="#1E293B"
    ).pack(side="left", padx=8)

    date_filter = tk.StringVar(value="This Month")

    filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=date_filter,
        values=["Last 7 Days", "This Month", "This Year"],
        state="readonly",
        width=18
    )
    filter_dropdown.pack(side="left", padx=8)

    # ---------- KPI cards ----------
    kpi_frame = tk.Frame(chart_window, bg="#F1F5F9")
    kpi_frame.pack(fill="x", padx=15, pady=10)

    # ---------- Chart area ----------
    chart_frame = tk.Frame(chart_window, bg="#F1F5F9")
    chart_frame.pack(fill="both", expand=True, padx=15, pady=5)

    figure = Figure(figsize=(10, 5), dpi=100, facecolor="#F1F5F9")
    chart_canvas = FigureCanvasTkAgg(figure, master=chart_frame)
    chart_widget = chart_canvas.get_tk_widget()
    chart_widget.configure(bg="#F1F5F9", highlightthickness=0)
    chart_widget.pack(fill="both", expand=True)

    colors = [
        "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6",
        "#EC4899", "#14B8A6", "#F97316", "#6366F1", "#84CC16"
    ]

    # ---------- Refresh ----------
    def refresh_analytics(event=None):
        selected_filter = date_filter.get()

        if selected_filter == "Last 7 Days":
            date_condition = """
                date(expense_date) IS NOT NULL
                AND date(expense_date) >= date('now', 'localtime', '-6 days')
                AND date(expense_date) <= date('now', 'localtime')
            """
        elif selected_filter == "This Year":
            date_condition = """
                strftime('%Y', expense_date) = strftime('%Y', 'now', 'localtime')
            """
        else:
            date_condition = """
                strftime('%Y-%m', expense_date) =
                strftime('%Y-%m', 'now', 'localtime')
            """

        conn = get_connection()
        try:
            cursor = conn.cursor()

            # Total for selected period
            cursor.execute(f"""
                SELECT COUNT(*), COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE user_id = ? AND {date_condition}
            """, (user_id,))
            total_count, total_amount = cursor.fetchone()
            total_amount = float(total_amount or 0)

            # Category data (highest spending first)
            cursor.execute(f"""
                SELECT COALESCE(category, 'Uncategorized'), SUM(amount)
                FROM expenses
                WHERE user_id = ? AND {date_condition}
                  AND amount IS NOT NULL
                GROUP BY COALESCE(category, 'Uncategorized')
                ORDER BY SUM(amount) DESC
            """, (user_id,))
            category_data = cursor.fetchall()

            # Daily / Monthly data
            if selected_filter == "This Year":
                cursor.execute(f"""
                    SELECT strftime('%Y-%m', expense_date), SUM(amount)
                    FROM expenses
                    WHERE user_id = ? AND {date_condition}
                      AND strftime('%Y-%m', expense_date) IS NOT NULL
                    GROUP BY strftime('%Y-%m', expense_date)
                    ORDER BY strftime('%Y-%m', expense_date)
                """, (user_id,))
                chart_title = "Monthly Expenses"
                x_title = "Month"
            else:
                cursor.execute(f"""
                    SELECT date(expense_date), SUM(amount)
                    FROM expenses
                    WHERE user_id = ? AND {date_condition}
                      AND date(expense_date) IS NOT NULL
                    GROUP BY date(expense_date)
                    ORDER BY date(expense_date)
                """, (user_id,))
                chart_title = "Daily Expenses"
                x_title = "Date"

            chart_data = cursor.fetchall()

            # Current month total (for KPI + budget)
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE user_id = ?
                  AND strftime('%Y-%m', expense_date) =
                      strftime('%Y-%m', 'now', 'localtime')
            """, (user_id,))
            monthly_total = float(cursor.fetchone()[0] or 0)

            # Budget
            now = datetime.now()
            cursor.execute("""
                SELECT budget_amount
                FROM budgets
                WHERE user_id = ? AND month = ? AND year = ?
            """, (user_id, now.month, now.year))
            budget_result = cursor.fetchone()
        finally:
            conn.close()

        highest_category = category_data[0][0] if category_data else "N/A"

        if budget_result and budget_result[0] is not None:
            budget_remaining = float(budget_result[0]) - monthly_total
        else:
            budget_remaining = 0.0

        # ---------- KPI cards ----------
        for widget in kpi_frame.winfo_children():
            widget.destroy()

        kpi_data = [
            ("Total Expenses", f"₹{total_amount:,.2f}"),
            ("This Month", f"₹{monthly_total:,.2f}"),
            ("Highest Category", str(highest_category)),
            ("Budget Remaining", f"₹{budget_remaining:,.2f}"),
        ]

        for title, value in kpi_data:
            value_color = "#1E293B"
            if title == "Budget Remaining" and budget_remaining < 0:
                value_color = "#DC2626"

            card = tk.Frame(kpi_frame, bg="white", padx=15, pady=12,
                            relief="raised", bd=1)
            card.pack(side="left", fill="both", expand=True, padx=8)

            tk.Label(card, text=title, font=("Arial", 10, "bold"),
                     bg="white", fg="#64748B").pack()
            tk.Label(card, text=value, font=("Arial", 15, "bold"),
                     bg="white", fg=value_color).pack(pady=6)

        # ---------- Charts ----------
        figure.clear()
        gs = figure.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.35)
        category_ax = figure.add_subplot(gs[0, 0])
        chart_ax = figure.add_subplot(gs[0, 1])

        for ax in (category_ax, chart_ax):
            ax.set_facecolor("#F1F5F9")

        # ----- Category pie (donut) with percentages -----
        pie_data = [
            (str(r[0]), float(r[1])) for r in category_data
            if r[0] is not None and r[1] is not None and float(r[1]) > 0
        ]

        if pie_data:
            pie_labels = [r[0] for r in pie_data]
            pie_values = [r[1] for r in pie_data]
            pie_total = sum(pie_values)
            pie_colors = [colors[i % len(colors)] for i in range(len(pie_values))]

            def show_pct(pct):
                # hide labels on very tiny slices so they don't overlap
                return f"{pct:.1f}%" if pct >= 4 else ""

            category_ax.pie(
                pie_values,
                colors=pie_colors,
                startangle=90,
                counterclock=False,
                autopct=show_pct,
                pctdistance=0.78,
                textprops={"fontsize": 9, "color": "white", "weight": "bold"},
                wedgeprops={"width": 0.45, "edgecolor": "#F1F5F9", "linewidth": 2}
            )
            category_ax.set_aspect("equal")

            # Total in the donut centre
            category_ax.text(
                0, 0, f"Total\n₹{pie_total:,.0f}",
                ha="center", va="center",
                fontsize=10, fontweight="bold", color="#1E293B"
            )

            legend_labels = [
                f"{name}  -  ₹{val:,.0f} ({val / pie_total * 100:.1f}%)"
                for name, val in zip(pie_labels, pie_values)
            ]
            category_ax.legend(
                legend_labels,
                loc="upper center",
                bbox_to_anchor=(0.5, -0.02),
                fontsize=8,
                frameon=False,
                ncol=1
            )
            category_ax.set_title(
                "Category Breakdown", fontsize=12,
                fontweight="bold", color="#1E293B"
            )
        else:
            category_ax.axis("off")
            category_ax.text(0.5, 0.5, "No Expense Data",
                             ha="center", va="center",
                             fontsize=12, color="#64748B",
                             transform=category_ax.transAxes)
            category_ax.set_title("Category Breakdown", fontsize=12,
                                  fontweight="bold", color="#1E293B")

        # ----- Bar chart -----
        valid_chart_data = [
            r for r in chart_data if r[0] is not None and r[1] is not None
        ]

        if valid_chart_data:
            labels = []
            for raw, _ in valid_chart_data:
                try:
                    if selected_filter == "This Year":
                        labels.append(datetime.strptime(raw, "%Y-%m").strftime("%b"))
                    else:
                        labels.append(datetime.strptime(raw, "%Y-%m-%d").strftime("%d %b"))
                except ValueError:
                    labels.append(str(raw))

            values = [float(r[1]) for r in valid_chart_data]

            bars = chart_ax.bar(labels, values, color="#3B82F6", width=0.6)

            # Value labels on top of bars (only when not crowded)
            if len(values) <= 12:
                for bar, val in zip(bars, values):
                    chart_ax.annotate(
                        f"₹{val:,.0f}",
                        (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        ha="center", va="bottom", fontsize=8,
                        xytext=(0, 3), textcoords="offset points",
                        color="#1E293B"
                    )

            chart_ax.set_title(chart_title, fontsize=12,
                               fontweight="bold", color="#1E293B")
            chart_ax.set_xlabel(x_title, fontsize=9)
            chart_ax.set_ylabel("Amount (₹)", fontsize=9)
            chart_ax.tick_params(axis="x", labelrotation=45, labelsize=8)
            chart_ax.tick_params(axis="y", labelsize=8)
            chart_ax.grid(axis="y", linestyle="--", alpha=0.4)
            chart_ax.set_axisbelow(True)
            chart_ax.margins(y=0.15)
            for side in ("top", "right"):
                chart_ax.spines[side].set_visible(False)
        else:
            chart_ax.axis("off")
            chart_ax.text(0.5, 0.5, "No Expense Data",
                          ha="center", va="center",
                          fontsize=12, color="#64748B",
                          transform=chart_ax.transAxes)
            chart_ax.set_title(chart_title, fontsize=12,
                               fontweight="bold", color="#1E293B")

        figure.subplots_adjust(left=0.07, right=0.97, top=0.90, bottom=0.25)
        chart_canvas.draw()

    filter_dropdown.bind("<<ComboboxSelected>>", refresh_analytics)
    refresh_analytics()
   

def open_dashboard(user):

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Expense Tracker Dashboard")
    dashboard_window.geometry("500x550")
    dashboard_window.resizable(True, True)

    # Main Frame
    main_frame = tk.Frame(dashboard_window)
    main_frame.pack(fill="both", expand=True)

    # Canvas
    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        main_frame,
        orient="vertical",
        command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable Frame
    scrollable_frame = tk.Frame(canvas)

    window_id = canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    # Update Scroll Region
    def update_scroll_region(event):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    scrollable_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfig(
            window_id,
            width=event.width
        )
    )

    # Mouse Wheel Scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind("<MouseWheel>", on_mousewheel)
    scrollable_frame.bind("<MouseWheel>", on_mousewheel)

    # Heading
    title_label = tk.Label(
        scrollable_frame,
        text="EXPENSE TRACKER",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=20)

    # Welcome Message
    welcome_label = tk.Label(
        scrollable_frame,
        text=f"Welcome, {user[1]}!",
        font=("Arial", 14)
    )
    welcome_label.pack(pady=10)

    # Add Expense
    add_button = tk.Button(
        scrollable_frame,
        text="ADD EXPENSE",
        width=25,
        height=2,
        command=lambda: open_add_expense_window(user[0])
    )
    add_button.pack(pady=8)

    # View Expenses
    view_button = tk.Button(
        scrollable_frame,
        text="VIEW EXPENSES",
        width=25,
        height=2,
        command=lambda: open_view_expenses_window(user[0])
    )
    view_button.pack(pady=8)

    # Update Expense
    update_button = tk.Button(
        scrollable_frame,
        text="UPDATE EXPENSE",
        width=25,
        height=2,
        command=lambda: open_update_expense_window(user[0])
    )
    update_button.pack(pady=8)

    # Delete Expense
    delete_button = tk.Button(
        scrollable_frame,
        text="DELETE EXPENSE",
        width=25,
        height=2,
        command=lambda: open_delete_expense_window(user[0])
    )
    delete_button.pack(pady=8)

    # Reports
    reports_button = tk.Button(
        scrollable_frame,
        text="REPORTS",
        width=25,
        height=2,
        command=lambda: open_reports_window(user[0])
    )
    reports_button.pack(pady=8)

    # Expense Analytics
    analytics_button = tk.Button(
        scrollable_frame,
        text="EXPENSE ANALYTICS",
        width=25,
        height=2,
        command=lambda: open_dashboard_charts_window(user[0])
    )
    analytics_button.pack(pady=8)

    # Monthly Budget
    budget_button = tk.Button(
        scrollable_frame,
        text="MONTHLY BUDGET",
        width=25,
        height=2,
        command=lambda: open_budget_window(user[0])
    )
    budget_button.pack(pady=8)

    # Income Management
    income_button = tk.Button(
        scrollable_frame,
        text="INCOME MANAGEMENT",
        width=25,
        height=2,
        command=lambda: open_add_income_window(user[0])
    )
    income_button.pack(pady=8)

    # View Income
    view_income_button = tk.Button(
        scrollable_frame,
        text="VIEW INCOME",
        width=25,
        height=2,
        command=lambda: open_view_income_window(user[0])
    )
    view_income_button.pack(pady=8)

    # Savings Calculator
    savings_button = tk.Button(
        scrollable_frame,
        text="SAVINGS CALCULATOR",
        width=25,
        height=2,
        command=lambda: open_savings_window(user[0])
    )
    savings_button.pack(pady=8)

    # Monthly Comparison
    comparison_button = tk.Button(
        scrollable_frame,
        text="MONTHLY COMPARISON",
        width=25,
        height=2,
        command=lambda: open_monthly_comparison_window(user[0])
    )
    comparison_button.pack(pady=8)
    
        # Export to Excel
    excel_button = tk.Button(
        scrollable_frame,
        text="EXPORT TO EXCEL",
        width=25,
        height=2,
        command=lambda: export_expenses_to_excel(user[0])
    )
    excel_button.pack(pady=8)
        # Export to PDF
    pdf_button = tk.Button(
        scrollable_frame,
        text="EXPORT TO PDF",
        width=25,
        height=2,
        command=lambda: export_expenses_to_pdf(user[0])
    )
    pdf_button.pack(pady=8)
    
    # Logout
    logout_button = tk.Button(
        scrollable_frame,
        text="LOGOUT",
        width=25,
        height=2,
        command=lambda: [
            dashboard_window.destroy(),
            open_login_window()
        ]
    )
    logout_button.pack(pady=20)

def open_login_window():

    login_window = tk.Toplevel(root)

    login_window.title("Login")
    login_window.geometry("400x300")

    # Heading
    title_label = tk.Label(
        login_window,
        text="LOGIN",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    # Email
    email_label = tk.Label(
        login_window,
        text="Email"
    )

    email_label.pack()

    email_entry = tk.Entry(
        login_window,
        width=30
    )

    email_entry.pack(pady=5)

    # Password
    password_label = tk.Label(
        login_window,
        text="Password"
    )

    password_label.pack()

    password_entry = tk.Entry(
        login_window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=5)

    # Login function
    def login():

        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:

            messagebox.showwarning(
                "Warning",
                "Please enter email and password."
            )

            return

        user = login_user(
            email,
            password
        )

        if user:

            messagebox.showinfo(
                "Success",
                f"Welcome, {user[1]}!"
            )

            login_window.destroy()
            open_dashboard(user)

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )

    # Login button
    login_button = tk.Button(
        login_window,
        text="LOGIN",
        width=20,
        command=login
    )
    login_button.pack(pady=20)

    # Back button
    back_button = tk.Button(
        login_window,
        text="BACK",
        width=20,
        command=login_window.destroy
    )

    back_button.pack()
def open_register_window():

    register_window = tk.Toplevel(root)

    register_window.title("Register")
    register_window.geometry("400x350")

    # Heading
    title_label = tk.Label(
        register_window,
        text="REGISTER",
        font=("Arial", 20, "bold")
    )

    title_label.pack(pady=20)

    # Name
    name_label = tk.Label(
        register_window,
        text="Name"
    )

    name_label.pack()

    name_entry = tk.Entry(
        register_window,
        width=30
    )

    name_entry.pack(pady=5)

    # Email
    email_label = tk.Label(
        register_window,
        text="Email"
    )

    email_label.pack()

    email_entry = tk.Entry(
        register_window,
        width=30
    )

    email_entry.pack(pady=5)

    # Password
    password_label = tk.Label(
        register_window,
        text="Password"
    )

    password_label.pack()

    password_entry = tk.Entry(
        register_window,
        width=30,
        show="*"
    )

    password_entry.pack(pady=5)

    # Register function
    def register():

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()

        # Empty field check
        if not name or not email or not password:

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return
        
        if "@" not in email or "." not in email.split("@")[-1]:

            messagebox.showwarning(
                "Warning",
                "Please enter a valid email address."
            )

            return
        
        if len(password) < 6:
            messagebox.showwarning(
                "Warning",
                "Password must be at least 6 characters long."
            )
            return
        
        # Call existing backend function
        success, message = register_user(
            name,
            email,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            register_window.destroy()

        else:

            messagebox.showerror(
                "Error",
                message
            )

    # Register button
    register_button = tk.Button(
        register_window,
        text="REGISTER",
        width=20,
        command=register
    )

    register_button.pack(pady=20)

    # Back button
    back_button = tk.Button(
        register_window,
        text="BACK",
        width=20,
        command=register_window.destroy
    )

    back_button.pack()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Expense Tracker")

root.geometry("500x400")


# Heading
title_label = tk.Label(
    root,
    text="EXPENSE TRACKER",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=30)


# Login button
login_button = tk.Button(
    root,
    text="LOGIN",
    width=20,
    height=2,
    command=open_login_window
)

login_button.pack(pady=10)


# Register button
register_button = tk.Button(
    root,
    text="REGISTER",
    width=20,
    height=2,
    command=open_register_window
)

register_button.pack(pady=10)


# Start GUI
root.mainloop()