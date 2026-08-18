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
# THEME
# =========================================================

from theme import apply_theme

apply_theme()


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.switch_page(
        "app.py"
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎓 Opportunity Hub")

st.sidebar.caption("Your Future, Our Priority")

st.sidebar.divider()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

if st.sidebar.button(
    "🏠  Dashboard",
    use_container_width=True
):

    st.switch_page(
        "pages/dashboard.py"
    )


if st.sidebar.button(
    "💼  Internships",
    use_container_width=True
):

    st.switch_page(
        "pages/Internships.py"
    )


if st.sidebar.button(
    "🎓  Scholarships",
    use_container_width=True
):

    st.switch_page(
        "pages/Scholarships.py"
    )


if st.sidebar.button(
    "🎤  Interview Prep",
    use_container_width=True
):

    st.switch_page(
        "pages/Interview.py"
    )


if st.sidebar.button(
    "🤖  Recommendations",
    use_container_width=True
):

    st.switch_page(
        "pages/Recommendations.py"
    )


if st.sidebar.button(
    "📄  Resume Builder",
    use_container_width=True
):

    st.switch_page(
        "pages/Resume.py"
    )


st.sidebar.divider()


# =========================================================
# QUICK ACTIONS
# =========================================================

st.sidebar.subheader("⚡ Quick Actions")


if st.sidebar.button(
    "🔍  Find Internships",
    use_container_width=True,
    key="side_internship"
):

    st.switch_page(
        "pages/Internships.py"
    )


if st.sidebar.button(
    "🎓  Find Scholarships",
    use_container_width=True,
    key="side_scholarship"
):

    st.switch_page(
        "pages/Scholarships.py"
    )


if st.sidebar.button(
    "📄  Create Resume",
    use_container_width=True,
    key="side_resume"
):

    st.switch_page(
        "pages/Resume.py"
    )


if st.sidebar.button(
    "🤖  Job Recommendations",
    use_container_width=True,
    key="side_jobs"
):

    st.switch_page(
        "pages/Recommendations.py"
    )


if st.sidebar.button(
    "🎤  Interview Practice",
    use_container_width=True,
    key="side_interview"
):

    st.switch_page(
        "pages/Interview.py"
    )


st.sidebar.divider()


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪  Logout",
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

st.title("Dashboard")

st.write(
    "Explore opportunities and build your career."
)

st.divider()


# =========================================================
# WELCOME BANNER
# =========================================================

st.success(
    "🎉 Welcome back! Let's explore new opportunities "
    "and achieve your goals."
)


# =========================================================
# STATISTICS
# =========================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    with st.container(border=True):

        st.subheader("💼 Internships")

        st.metric(
            "Active Opportunities",
            "120+"
        )


with c2:

    with st.container(border=True):

        st.subheader("🎓 Scholarships")

        st.metric(
            "Available Now",
            "85+"
        )


with c3:

    with st.container(border=True):

        st.subheader("🎤 Interviews")

        st.metric(
            "Practice Sessions",
            "10"
        )


with c4:

    with st.container(border=True):

        st.subheader("✨ Matches")

        st.metric(
            "Profile Strength",
            "98%"
        )


st.divider()


# =========================================================
# QUICK ACTION CARDS
# =========================================================

st.subheader("🚀 Quick Actions")


# =========================================================
# ROW 1
# =========================================================

col1, col2, col3 = st.columns(3)


# ---------------------------------------------------------
# INTERNSHIP
# ---------------------------------------------------------

with col1:

    with st.container(border=True):

        st.image(
            "image/internship_icon.png",
            use_container_width=True
        )

        st.subheader("Find Internships")

        st.write(
            "Discover internships that match "
            "your skills and interests."
        )

        if st.button(
            "Explore Internships →",
            use_container_width=True,
            key="dashboard_internship"
        ):

            st.switch_page(
                "pages/Internships.py"
            )


# ---------------------------------------------------------
# SCHOLARSHIP
# ---------------------------------------------------------

with col2:

    with st.container(border=True):

        st.image(
            "image/scholarship_icon.png",
            use_container_width=True
        )

        st.subheader("Find Scholarships")

        st.write(
            "Find scholarships that fit your "
            "profile and achievements."
        )

        if st.button(
            "Explore Scholarships →",
            use_container_width=True,
            key="dashboard_scholarship"
        ):

            st.switch_page(
                "pages/Scholarships.py"
            )


# ---------------------------------------------------------
# RESUME
# ---------------------------------------------------------

with col3:

    with st.container(border=True):

        st.image(
            "image/resume_icon.png",
            use_container_width=True
        )

        st.subheader("Create Resume")

        st.write(
            "Build a professional resume "
            "that stands out."
        )

        if st.button(
            "Create Resume →",
            use_container_width=True,
            key="dashboard_resume"
        ):

            st.switch_page(
                "pages/Resume.py"
            )


# =========================================================
# ROW 2
# =========================================================

col4, col5, col6 = st.columns(3)


# ---------------------------------------------------------
# JOB RECOMMENDATIONS
# ---------------------------------------------------------

with col4:

    with st.container(border=True):

        st.image(
            "image/upload_resume.png",
            use_container_width=True
        )

        st.subheader("Job Recommendations")

        st.write(
            "Get AI-powered job recommendations "
            "just for you."
        )

        if st.button(
            "View Recommendations →",
            use_container_width=True,
            key="dashboard_jobs"
        ):

            st.switch_page(
                "pages/Recommendations.py"
            )


# ---------------------------------------------------------
# INTERVIEW
# ---------------------------------------------------------

with col5:

    with st.container(border=True):

        st.image(
            "image/interview_icon.png",
            use_container_width=True
        )

        st.subheader("Interview Practice")

        st.write(
            "Practice interviews and improve "
            "your confidence."
        )

        if st.button(
            "Start Practice →",
            use_container_width=True,
            key="dashboard_interview"
        ):

            st.switch_page(
                "pages/Interview.py"
            )


            

# =========================================================
# PLATFORM FEATURES
# =========================================================

st.divider()

st.subheader("✨ Platform Features")


f1, f2, f3, f4 = st.columns(4)


with f1:

    with st.container(border=True):

        st.subheader("🎓 Scholarships")

        st.write(
            "Find scholarship opportunities "
            "for your education."
        )


with f2:

    with st.container(border=True):

        st.subheader("💼 Internships")

        st.write(
            "Discover internship opportunities "
            "based on your interests."
        )


with f3:

    with st.container(border=True):

        st.subheader("📄 Resume Builder")

        st.write(
            "Create and manage your professional "
            "resume."
        )


with f4:

    with st.container(border=True):

        st.subheader("🤖 AI Recommendations")

        st.write(
            "Get suitable job recommendations "
            "using machine learning."
        )
