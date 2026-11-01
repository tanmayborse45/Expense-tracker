import sqlite3
import hashlib

from database import get_connection


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, hashed_password))

        conn.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:

        return False, "Email already registered."

    except Exception as e:

        return False, f"Registration failed: {e}"

    finally:

        conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = ?
        AND password = ?
    """, (email, hashed_password))

    user = cursor.fetchone()

    conn.close()

    return user
