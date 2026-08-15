import streamlit as st
import sqlite3
import hashlib
import os


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "users.db"
)


# =========================================================
# CREATE DATABASE
# =========================================================

def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# REGISTER USER
# =========================================================

def register_user(email, password):

    email = email.strip().lower()

    if not email:

        return False, "Email cannot be empty."

    if len(password) < 6:

        return False, (
            "Password must contain at least 6 characters."
        )

    hashed_password = hash_password(
        password
    )

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (email, password)
            VALUES (?, ?)
            """,
            (
                email,
                hashed_password
            )
        )

        conn.commit()
        conn.close()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Email already exists."

    except Exception as e:

        return False, str(e)


# =========================================================
# LOGIN USER
# =========================================================

def login_user(email, password):

    email = email.strip().lower()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, email, password
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return False

    entered_password = hash_password(
        password
    )

    if user[2] == entered_password:

        st.session_state["logged_in"] = True

        st.session_state["email"] = user[1]

        return True

    return False


# =========================================================
# LOGOUT
# =========================================================

def logout_user():

    st.session_state["logged_in"] = False

    st.session_state["email"] = ""

    # Optional page state cleanup
    if "page" in st.session_state:

        st.session_state["page"] = "login"


# =========================================================
# CHECK LOGIN
# =========================================================

def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


# =========================================================
# REQUIRE LOGIN
# =========================================================

def require_login():

    create_database()

    if not is_logged_in():

        st.warning(
            "🔐 Please login to access this page."
        )

        st.stop()