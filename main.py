from database import create_tables
from auth import register_user, login_user

from expenses import (
    add_expense,
    view_expenses,
    update_expense,
    delete_expense
)
from reports import reports_menu
from budget import budget_menu



# -------------------------
# REGISTER
# -------------------------

def register():

    print("\n========================")
    print("       REGISTER")
    print("========================")

    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    success, message = register_user(
        name,
        email,
        password
    )

    print("\n" + message)


# -------------------------
# LOGIN
# -------------------------

def login():

    print("\n========================")
    print("         LOGIN")
    print("========================")

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = login_user(
        email,
        password
    )

    if user:

        print("\nLogin successful!")
        print(f"Welcome, {user[1]}!")

        return user

    else:

        print("\nInvalid email or password.")

        return None


# -------------------------
# EXPENSE MENU
# -------------------------

def expense_menu(user):

    user_id = user[0]
    user_name = user[1]

    while True:

        print("\n================================")
        print(f"       WELCOME, {user_name}")
        print("================================")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Search & Reports")
        print("6. Monthly Budget")
        print("7. Logout")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            add_expense(user_id)

        elif choice == "2":

            view_expenses(user_id)

        elif choice == "3":

            update_expense(user_id)

        elif choice == "4":

            delete_expense(user_id)

        elif choice == "5":

            reports_menu(user_id)

        elif choice == "6":

            budget_menu(user_id)

        elif choice == "7":

            print("\nLogged out successfully.")
            break

        else:

            print("\nInvalid choice. Please try again.")


# -------------------------
# MAIN PROGRAM
# -------------------------

def main():

    # Database aur tables create karna
    create_tables()

    while True:

        print("\n")
        print("==============================")
        print("       EXPENSE TRACKER")
        print("==============================")

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            register()

        elif choice == "2":

            user = login()

            if user:

                print("\nYou are now logged in.")

                expense_menu(user)

        elif choice == "3":

            print("\nThank you for using Expense Tracker!")
            break

        else:

            print("\nInvalid choice. Please try again.")


# -------------------------
# PROGRAM START
# -------------------------

if __name__ == "__main__":
    main()
