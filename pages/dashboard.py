import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Opportunity Hub",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.switch_page(
        "app.py"
    )


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #1f3c88;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

.card {
    padding: 25px;
    border-radius: 15px;
    background-color: #ffffff;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.card-title {
    font-size: 25px;
    font-weight: 600;
    color: #263238;
}

.card-text {
    color: #666;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Menu")

st.sidebar.divider()


# HOME

if st.sidebar.button(
    "🏠 Home",
    use_container_width=True
):

    st.switch_page(
        "pages/dashboard.py"
    )


# SCHOLARSHIPS

if st.sidebar.button(
    "🎓 Scholarships",
    use_container_width=True
):

    st.switch_page(
        "pages/Scholarships.py"
    )


# INTERNSHIPS

if st.sidebar.button(
    "💼 Internships",
    use_container_width=True
):

    st.switch_page(
        "pages/Internships.py"
    )


# RESUME

if st.sidebar.button(
    "📄 Create Resume",
    use_container_width=True
):

    st.switch_page(
        "pages/Resume.py"
    )


# RECOMMENDATIONS

if st.sidebar.button(
    "🤖 Job Recommendations",
    use_container_width=True
):

    st.switch_page(
        "pages/Recommendations.py"
    )
 # INTERVIEW

if st.sidebar.button(
    "📝 Interviews",
    use_container_width=True
):
    st.switch_page(
        "pages/Interview.py"
    )



st.sidebar.divider()


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.session_state.google_page = False

    st.switch_page(
        "app.py"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🎓 Student Opportunity Hub'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'Your single platform for discovering scholarships, '
    'internships, resumes and jobs.'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# =========================================================
# WELCOME
# =========================================================

st.success(
    "🎉 Login successful! Welcome to Student Opportunity Hub."
)


# =========================================================
# SCHOLARSHIP + INTERNSHIP
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# SCHOLARSHIPS
# =========================================================

with col1:
    st.markdown(
    """
    <div class="card">
    """,
    unsafe_allow_html=True
)

# Image
    st.image(
        "images/scholarship_icon.png",
        use_container_width=True
)



    if st.button(
        "🔎 Find Scholarships",
        use_container_width=True,
        key="scholarship_home"
    ):

        st.switch_page(
            "pages/Scholarships.py"
        )


# =========================================================
# INTERNSHIPS
# =========================================================

with col2:
    st.markdown(
    """
    <div class="card">
    """,
    unsafe_allow_html=True
)

# Image
    st.image(
        "images/internship_icon.png",
        use_container_width=True
)




    if st.button(
        "🔎 Find Internships",
        use_container_width=True,
        key="internship_home"
    ):

        st.switch_page(
            "pages/Internships.py"
        )


# =========================================================
# RESUME + JOBS
# =========================================================

col3, col4 = st.columns(2)


# =========================================================
# RESUME
# =========================================================

with col3:
    st.markdown(
    """
    <div class="card">
    """,
    unsafe_allow_html=True
)

# Image
    st.image(
        "images/resume_icon.png",
        use_container_width=True
)




    if st.button(
        "📄 Create Resume",
        use_container_width=True,
        key="resume_home"
    ):

        st.switch_page(
            "pages/Resume.py"
        )


# =========================================================
# JOB RECOMMENDATIONS
# =========================================================

with col4:
    st.markdown(
    """
    <div class="card">
    """,
    unsafe_allow_html=True
)

# Image
    st.image(
        "images/upload_resume.png",
        use_container_width=True
)




    if st.button(
        "🤖 Find Recommended Jobs",
        use_container_width=True,
        key="jobs_home"
    ):

        st.switch_page(
            "pages/Recommendations.py"
        )
# =========================================================
# INTERVIEW CARD
# =========================================================

col5, col6 = st.columns(2)

with col5:
    st.markdown(
        """
        <div class="card">
        """,
        unsafe_allow_html=True
    )

    # Image
    st.image(
        "images/interview_icon.png",  
        use_container_width=True
    )

    if st.button(
        "📝 Practice Interviews",
        use_container_width=True,
        key="interview_home"
    ):
        st.switch_page(
            "pages/Interview.py"
        )



# =========================================================
# FEATURES
# =========================================================

st.divider()

st.header("✨ Platform Features")


f1, f2, f3, f4 = st.columns(4)


with f1:

    st.info(
        "🎓 **Scholarships**\n\n"
        "Latest scholarship updates."
    )


with f2:

    st.info(
        "💼 **Internships**\n\n"
        "Find internship opportunities."
    )


with f3:

    st.info(
        "📄 **Resume Builder**\n\n"
        "Create your resume."
    )


with f4:

    st.info(
        "🤖 **Job Recommendations**\n\n"
        "Get suitable jobs."
    )
