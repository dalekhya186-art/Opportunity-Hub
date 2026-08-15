import streamlit as st
import sqlite3
import hashlib
import re
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title=" Opportunity Hub",
    page_icon="🎓",
    layout="centered"
)


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
# DATABASE
# =========================================================

conn = sqlite3.connect(
    DB_PATH,
    timeout=10
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

conn.commit()


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# EMAIL VALIDATION
# =========================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(
        pattern,
        email
    )


# =========================================================
# REGISTER USER
# =========================================================

def register_user(email, password):

    email = email.strip().lower()

    hashed_password = hash_password(
        password
    )

    try:

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

        return True

    except sqlite3.IntegrityError:

        return False


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "login"


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "google_page" not in st.session_state:

    st.session_state.google_page = False


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 430px;
        padding-top: 35px;
    }

    .logo {
        text-align: center;
        margin-bottom: 25px;
    }

    h1 {
        text-align: center;
        font-size: 25px !important;
    }

    .stTextInput input {
        height: 42px;
        border-radius: 6px;
    }

    .stButton button {
        width: 100%;
        height: 42px;
        border-radius: 6px;
    }

    .account-card {
        border: 1px solid #dadce0;
        border-radius: 10px;
        padding: 14px;
        margin: 10px 0;
    }

    .account-name {
        font-size: 15px;
        font-weight: 500;
    }

    .account-email {
        font-size: 13px;
        color: #666;
    }

    .google-title {
        text-align: center;
        font-size: 24px;
        margin-top: 10px;
    }

    .google-subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGO
# =========================================================

def show_logo(icon="🎓"):

    st.markdown(
        f"""
        <div style="
            width:55px;
            height:55px;
            border-radius:50%;
            border:3px solid #4285f4;
            display:flex;
            align-items:center;
            justify-content:center;
            margin:auto;
            font-size:28px;
        ">
            {icon}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    show_logo()

    st.title(
        "Log in to your account"
    )


    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    email = st.text_input(
        "Email",
        key="login_email"
    )


    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )


    # -----------------------------------------------------
    # REMEMBER ME
    # -----------------------------------------------------

    st.checkbox(
        "Remember me",
        key="remember_me"
    )


    # -----------------------------------------------------
    # SIGN IN
    # -----------------------------------------------------

    if st.button(
        "Sign in",
        key="sign_in"
    ):

        if email == "" or password == "":

            st.warning(
                "Please enter email and password."
            )

        else:

            email = email.strip().lower()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE email = ?
                """,
                (email,)
            )

            user = cursor.fetchone()


            if user is None:

                st.error(
                    "Account not created. First Signup cheyyi."
                )

            else:

                entered_password = hash_password(
                    password
                )


                if user[2] == entered_password:

                    st.session_state.logged_in = True

                    st.session_state.email = user[1]

                    st.session_state.page = "dashboard"

                    st.switch_page(
                        "pages/dashboard.py"
                    )

                else:

                    st.error(
                        "Incorrect password."
                    )


    # -----------------------------------------------------
    # OR
    # -----------------------------------------------------

    st.markdown(
        """
        <div style="
            text-align:center;
            margin:18px 0;
            color:#999;
        ">
            or
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # GOOGLE LOGIN
    # -----------------------------------------------------

    if st.button(
        "Continue with Google",
        key="google_login"
    ):

        st.session_state.google_page = True

        st.rerun()


    # -----------------------------------------------------
    # SIGN UP TEXT
    # -----------------------------------------------------

    st.markdown(
        """
        <p style="text-align:center;">
            Don't have an account?
        </p>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SIGN UP BUTTON
    # -----------------------------------------------------

    if st.button(
        "Sign up",
        key="go_signup"
    ):

        st.session_state.page = "signup"

        st.rerun()


# =========================================================
# GOOGLE OAUTH IMPORTS
# =========================================================

try:

    from google_auth_oauthlib.flow import Flow
    from google.oauth2 import id_token
    from google.auth.transport import requests

    GOOGLE_AVAILABLE = True

except ImportError:

    GOOGLE_AVAILABLE = False


# =========================================================
# GOOGLE LOGIN
# =========================================================

def google_login():

    if not GOOGLE_AVAILABLE:

        st.error(
            "Google login package is not installed."
        )

        return


    client_secrets_file = os.path.join(
        BASE_DIR,
        "client_secret.json"
    )


    if not os.path.exists(
        client_secrets_file
    ):

        st.error(
            "client_secret.json not found."
        )

        return


    flow = Flow.from_client_secrets_file(

        client_secrets_file,

        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email"
        ],

        redirect_uri="http://localhost:8501"
    )


    auth_url, _ = flow.authorization_url(
        prompt="consent"
    )


    st.link_button(
        "🌈 Continue with Google",
        auth_url,
        use_container_width=True
    )


# =========================================================
# HANDLE GOOGLE CALLBACK
# =========================================================

def handle_google_callback(code):

    if not GOOGLE_AVAILABLE:

        st.error(
            "Google OAuth package is not installed."
        )

        return


    client_secrets_file = os.path.join(
        BASE_DIR,
        "client_secret.json"
    )


    if not os.path.exists(
        client_secrets_file
    ):

        st.error(
            "client_secret.json not found."
        )

        return


    try:

        flow = Flow.from_client_secrets_file(

            client_secrets_file,

            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email"
            ],

            redirect_uri="http://localhost:8501"
        )


        flow.fetch_token(
            code=code
        )


        credentials = flow.credentials


        user_info = id_token.verify_oauth2_token(

            credentials.id_token,

            requests.Request()
        )


        email = user_info["email"]

        email = email.strip().lower()


        # ---------------------------------------------
        # CREATE GOOGLE USER IF NOT EXISTS
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )


        existing_user = cursor.fetchone()


        if existing_user is None:

            register_user(
                email,
                "google_oauth_dummy_password"
            )


        # ---------------------------------------------
        # LOGIN
        # ---------------------------------------------

        st.session_state.logged_in = True

        st.session_state.email = email

        st.session_state.page = "dashboard"

        st.session_state.google_page = False


        # ---------------------------------------------
        # CLEAR QUERY PARAMS
        # ---------------------------------------------

        st.query_params.clear()


        st.switch_page(
            "pages/dashboard.py"
        )


    except Exception as e:

        st.error(
            "Google login failed."
        )

        st.exception(e)


# =========================================================
# GOOGLE ACCOUNTS PAGE
# =========================================================

def google_accounts():

    show_logo()


    st.markdown(
        """
        <div class="google-title">
            Choose an account
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="google-subtitle">
            to continue to your application
        </div>
        """,
        unsafe_allow_html=True
    )


    google_login()


    st.divider()


    if st.button(
        "⬅ Back to Login",
        key="back_google"
    ):

        st.session_state.google_page = False

        st.session_state.page = "login"

        st.rerun()


# =========================================================
# SIGNUP PAGE
# =========================================================

def signup_page():

    show_logo()

    st.title(
        "Create your account"
    )


    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    email = st.text_input(
        "Email",
        key="signup_email"
    )


    # -----------------------------------------------------
    # PASSWORD
    # -----------------------------------------------------

    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )


    # -----------------------------------------------------
    # CONFIRM PASSWORD
    # -----------------------------------------------------

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )


    # -----------------------------------------------------
    # CREATE ACCOUNT
    # -----------------------------------------------------

    if st.button(
        "Create Account",
        key="create_account"
    ):

        if (
            email == ""
            or password == ""
            or confirm_password == ""
        ):

            st.warning(
                "Please fill all fields."
            )


        elif not valid_email(email):

            st.error(
                "Please enter a valid email."
            )


        elif len(password) < 6:

            st.error(
                "Password must contain at least 6 characters."
            )


        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )


        else:

            success = register_user(
                email,
                password
            )


            if success:

                st.success(
                    "Account successfully created! 🎉"
                )

                st.session_state.page = "login"

                st.rerun()

            else:

                st.error(
                    "This account already exists."
                )


    # -----------------------------------------------------
    # BACK TO LOGIN
    # -----------------------------------------------------

    if st.button(
        "Back to Login",
        key="back_to_login"
    ):

        st.session_state.page = "login"

        st.rerun()


# =========================================================
# GOOGLE CALLBACK
# =========================================================
#
# IMPORTANT:
# Old:
# st.experimental_get_query_params()
#
# New:
# st.query_params
#
# =========================================================

params = st.query_params

if "code" in params:

    google_code = params.get("code")

    if google_code:

        handle_google_callback(
            google_code
        )


# =========================================================
# MAIN APPLICATION
# =========================================================

if st.session_state.logged_in:

    st.switch_page(
        "pages/dashboard.py"
    )


elif st.session_state.google_page:

    google_accounts()


elif st.session_state.page == "login":

    login_page()


elif st.session_state.page == "signup":

    signup_page()