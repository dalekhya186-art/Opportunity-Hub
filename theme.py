import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background: #f8f9ff !important;
        }

        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #f4f1ff 0%,
                #f8f7ff 100%
            ) !important;

            border-right: 1px solid #e5e1ff;
        }

        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }


        /* =====================================================
           SIDEBAR HEADINGS
        ===================================================== */

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #18264d !important;
        }


        /* =====================================================
           SIDEBAR BUTTONS
        ===================================================== */

        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            min-height: 44px !important;

            background: transparent !important;

            color: #24345d !important;

            border: none !important;
            border-radius: 10px !important;

            font-size: 15px !important;
            font-weight: 500 !important;

            text-align: left !important;

            transition: all 0.2s ease;
        }

        /* SIDEBAR BUTTON TEXT */
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span,
        section[data-testid="stSidebar"] .stButton > button div {
            color: #24345d !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #e8e2ff !important;
            color: #5b3fd1 !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover p,
        section[data-testid="stSidebar"] .stButton > button:hover span,
        section[data-testid="stSidebar"] .stButton > button:hover div {
            color: #5b3fd1 !important;
        }


        /* =====================================================
           NORMAL DASHBOARD BUTTONS
        ===================================================== */

        .stButton > button {
            width: 100% !important;

            min-height: 45px !important;

            border-radius: 12px !important;

            border: none !important;

            background: linear-gradient(
                135deg,
                #7657e8,
                #6244c7
            ) !important;

            color: #ffffff !important;

            font-weight: 700 !important;

            font-size: 15px !important;

            padding: 0.65rem 1rem !important;

            box-shadow:
                0 4px 12px rgba(98, 68, 199, 0.25) !important;

            transition: all 0.2s ease;
        }


        /* =====================================================
           IMPORTANT:
           DASHBOARD BUTTON TEXT
        ===================================================== */

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: #ffffff !important;

            font-weight: 700 !important;

            font-size: 15px !important;
        }


        /* =====================================================
           BUTTON HOVER
        ===================================================== */

        .stButton > button:hover {
            background: linear-gradient(
                135deg,
                #6244c7,
                #5035ad
            ) !important;

            color: #ffffff !important;

            transform: translateY(-1px);

            box-shadow:
                0 6px 16px rgba(98, 68, 199, 0.35) !important;
        }


        /* =====================================================
           IMPORTANT:
           HOVER TEXT ALSO WHITE
        ===================================================== */

        .stButton > button:hover p,
        .stButton > button:hover span,
        .stButton > button:hover div {
            color: #ffffff !important;
        }


        /* =====================================================
           BUTTON FOCUS / ACTIVE
        ===================================================== */

        .stButton > button:focus,
        .stButton > button:active {
            color: #ffffff !important;

            background: linear-gradient(
                135deg,
                #6244c7,
                #5035ad
            ) !important;
        }

        .stButton > button:focus p,
        .stButton > button:focus span,
        .stButton > button:focus div,
        .stButton > button:active p,
        .stButton > button:active span,
        .stButton > button:active div {
            color: #ffffff !important;
        }


        /* =====================================================
           HEADINGS
        ===================================================== */

        h1,
        h2,
        h3 {
            color: #17213c !important;
        }


        /* =====================================================
           NORMAL TEXT
        ===================================================== */

        p {
            color: #4b5875;
        }


        /* =====================================================
           EXTRA PROTECTION FOR BUTTON TEXT
           Must stay AFTER normal p rule
        ===================================================== */

        .stButton > button p {
            color: #ffffff !important;
        }

        .stButton > button span {
            color: #ffffff !important;
        }

        .stButton > button div {
            color: #ffffff !important;
        }


        /* =====================================================
           INPUTS
        ===================================================== */

        input,
        textarea {
            border-radius: 10px !important;

            border: 1px solid #e3e6f0 !important;
        }

        input:focus,
        textarea:focus {
            border-color: #7656e8 !important;

            box-shadow:
                0 0 0 2px rgba(118, 86, 232, 0.12) !important;
        }


        /* =====================================================
           SELECT BOX
        ===================================================== */

        div[data-baseweb="select"] > div {
            border-radius: 10px !important;

            border-color: #e3e6f0 !important;
        }


        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 12px !important;
        }


        /* =====================================================
           DIVIDER
        ===================================================== */

        hr {
            border-color: #e8e8f2 !important;
        }


        /* =====================================================
           DASHBOARD CARDS
        ===================================================== */

        .dashboard-card {
            background: #ffffff;

            border: 1px solid #ececf5;

            border-radius: 18px;

            padding: 22px;

            box-shadow:
                0 5px 20px rgba(38, 35, 80, 0.06);

            margin-bottom: 18px;

            transition: all 0.2s ease;
        }

        .dashboard-card:hover {
            transform: translateY(-2px);

            box-shadow:
                0 10px 28px rgba(38, 35, 80, 0.10);
        }


        /* =====================================================
           STAT CARDS
        ===================================================== */

        .stat-card {
            background: #ffffff;

            border: 1px solid #ececf5;

            border-radius: 18px;

            padding: 20px;

            min-height: 145px;

            box-shadow:
                0 5px 18px rgba(38, 35, 80, 0.06);
        }

        .stat-icon {
            font-size: 27px;

            display: inline-flex;

            width: 52px;
            height: 52px;

            align-items: center;
            justify-content: center;

            border-radius: 50%;

            background: #f0ecff;
        }

        .stat-title {
            color: #596681;

            font-size: 14px;

            margin-top: 12px;
        }

        .stat-number {
            color: #17213c;

            font-size: 29px;

            font-weight: 700;

            margin-top: 2px;
        }

        .stat-sub {
            font-size: 13px;

            margin-top: 4px;

            color: #6c4ce3;
        }


        /* =====================================================
           WELCOME BANNER
        ===================================================== */

        .welcome-banner {
            background: linear-gradient(
                100deg,
                #f2efff,
                #f8f7ff
            );

            border: 1px solid #e8e1ff;

            border-radius: 18px;

            padding: 25px 30px;

            margin-bottom: 22px;
        }

        .welcome-title {
            color: #17213c;

            font-size: 24px;

            font-weight: 700;
        }

        .welcome-text {
            color: #5c6880;

            font-size: 15px;

            margin-top: 5px;
        }


        /* =====================================================
           QUICK ACTION CARDS
        ===================================================== */

        .quick-card {
            background: #ffffff;

            border: 1px solid #ececf5;

            border-radius: 16px;

            padding: 20px;

            min-height: 135px;

            box-shadow:
                0 4px 15px rgba(38, 35, 80, 0.05);
        }

        .quick-icon {
            font-size: 28px;
        }

        .quick-title {
            color: #17213c;

            font-size: 17px;

            font-weight: 700;

            margin-top: 7px;
        }

        .quick-text {
            color: #667085;

            font-size: 14px;

            line-height: 1.5;

            margin-top: 5px;
        }


        /* =====================================================
           SEARCH BOX
        ===================================================== */

        .search-box {
            background: #ffffff;

            border: 1px solid #e6e7f0;

            border-radius: 25px;

            padding: 12px 20px;

            color: #788299;

            text-align: center;

            font-size: 14px;

            box-shadow:
                0 3px 12px rgba(38, 35, 80, 0.04);
        }


        /* =====================================================
           SIDEBAR BRAND
        ===================================================== */

        .sidebar-brand {
            text-align: center;

            padding: 10px 5px 20px;
        }

        .sidebar-brand-icon {
            font-size: 42px;
        }

        .sidebar-brand-title {
            font-size: 19px;

            font-weight: 700;

            color: #18264d;
        }

        .sidebar-brand-subtitle {
            font-size: 12px;

            color: #69758e;
        }


        /* =====================================================
           FEATURE BOX
        ===================================================== */

        .feature-box {
            background: #ffffff;

            border: 1px solid #ececf5;

            border-radius: 15px;

            padding: 18px;

            min-height: 120px;

            box-shadow:
                0 4px 15px rgba(38, 35, 80, 0.05);
        }

        .feature-title {
            color: #17213c;

            font-size: 16px;

            font-weight: 700;
        }

        .feature-text {
            color: #69758e;

            font-size: 13px;

            margin-top: 7px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )