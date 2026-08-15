import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO


from auth import require_login

require_login()
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Create Resume",
    page_icon="📄",
    layout="wide"
)


# =====================================================
# LOGIN CHECK
# =====================================================

if not st.session_state.get("logged_in", False):

    st.warning("🔐 Please login first.")
    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎓 Opportunity Hub")

st.sidebar.page_link(
    "app.py",
    label="🏠 Home"
)

st.sidebar.page_link(
    "pages/Scholarships.py",
    label="🎓 Scholarships"
)

st.sidebar.page_link(
    "pages/Internships.py",
    label="💼 Internships"
)

st.sidebar.page_link(
    "pages/Resume.py",
    label="📄 Create Resume"
)

st.sidebar.page_link(
    "pages/Recommendations.py",
    label="🤖 Job Recommendations"
)


# =====================================================
# PDF CREATION FUNCTION
# =====================================================

def create_resume_pdf(
    name,
    email,
    phone,
    city,
    linkedin,
    github,
    career_objective,
    education,
    skills,
    projects,
    experience,
    certifications,
    achievements
):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    # ---------------------------------------------
    # HEADER
    # ---------------------------------------------

    y = height - 50

    pdf.setFillColor(
        colors.black
    )

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        50,
        y,
        name
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        9
    )

    contact = (
        f"{email} | {phone} | {city}"
    )

    pdf.drawString(
        50,
        y,
        contact[:110]
    )

    y -= 16

    if linkedin:

        pdf.drawString(
            50,
            y,
            "LinkedIn: " + linkedin
        )

        y -= 14

    if github:

        pdf.drawString(
            50,
            y,
            "GitHub: " + github
        )

        y -= 20


    # ---------------------------------------------
    # HELPER FUNCTION
    # ---------------------------------------------

    def add_section(
        title,
        content
    ):

        nonlocal y

        if not content.strip():

            return

        if y < 90:

            pdf.showPage()

            y = height - 50

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.drawString(
            50,
            y,
            title.upper()
        )

        y -= 8

        pdf.line(
            50,
            y,
            width - 50,
            y
        )

        y -= 18

        pdf.setFont(
            "Helvetica",
            9
        )

        lines = content.split("\n")

        for line in lines:

            if not line.strip():

                y -= 8
                continue

            if y < 55:

                pdf.showPage()

                y = height - 50

            pdf.drawString(
                60,
                y,
                line[:105]
            )

            y -= 14

        y -= 10


    # ---------------------------------------------
    # SECTIONS
    # ---------------------------------------------

    add_section(
        "Career Objective",
        career_objective
    )

    add_section(
        "Education",
        education
    )

    add_section(
        "Skills",
        skills
    )

    add_section(
        "Projects",
        projects
    )

    add_section(
        "Experience",
        experience
    )

    add_section(
        "Certifications",
        certifications
    )

    add_section(
        "Achievements",
        achievements
    )

    pdf.save()

    buffer.seek(0)

    return buffer


# =====================================================
# PAGE TITLE
# =====================================================

st.title(
    "📄 Resume Builder"
)

st.write(
    "Create a professional resume and "
    "download it as a PDF."
)

st.divider()


# =====================================================
# PERSONAL INFORMATION
# =====================================================

st.header(
    "👤 Personal Information"
)

col1, col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Full Name *",
        placeholder="Enter your full name"
    )

    email = st.text_input(
        "Email *",
        placeholder="example@gmail.com"
    )

    phone = st.text_input(
        "Phone Number",
        placeholder="+91 XXXXX XXXXX"
    )


with col2:

    city = st.text_input(
        "City",
        placeholder="Hyderabad"
    )

    linkedin = st.text_input(
        "LinkedIn Profile",
        placeholder="https://linkedin.com/in/..."
    )

    github = st.text_input(
        "GitHub Profile",
        placeholder="https://github.com/..."
    )


# =====================================================
# CAREER OBJECTIVE
# =====================================================

st.header(
    "🎯 Career Objective"
)

career_objective = st.text_area(
    "Write your career objective",
    placeholder=(
        "Motivated student seeking an opportunity "
        "to apply technical skills and gain "
        "professional experience."
    ),
    height=100
)


# =====================================================
# EDUCATION
# =====================================================

st.header(
    "🎓 Education"
)

education = st.text_area(
    "Education Details",
    placeholder=(
        "B.Tech in Computer Science\n"
        "ABC Engineering College\n"
        "2023 - 2027\n"
        "CGPA: 8.5"
    ),
    height=150
)


# =====================================================
# SKILLS
# =====================================================

st.header(
    "🛠️ Technical Skills"
)

skills = st.text_area(
    "Skills",
    placeholder=(
        "Python\n"
        "SQL\n"
        "Machine Learning\n"
        "HTML, CSS\n"
        "JavaScript\n"
        "Git & GitHub"
    ),
    height=150
)


# =====================================================
# PROJECTS
# =====================================================

st.header(
    "📊 Projects"
)

projects = st.text_area(
    "Project Details",
    placeholder=(
        "Student Opportunity Hub\n"
        "Developed a Streamlit website to help "
        "students find scholarships, internships "
        "and job opportunities.\n\n"
        "Technologies: Python, Streamlit, SQLite"
    ),
    height=180
)


# =====================================================
# EXPERIENCE
# =====================================================

st.header(
    "💼 Experience / Internship"
)

experience = st.text_area(
    "Experience",
    placeholder=(
        "Software Development Intern\n"
        "ABC Technologies\n"
        "May 2026 - July 2026\n"
        "Worked on web application development."
    ),
    height=150
)


# =====================================================
# CERTIFICATIONS
# =====================================================

st.header(
    "🏆 Certifications"
)

certifications = st.text_area(
    "Certifications",
    placeholder=(
        "Python Programming - XYZ Institute\n"
        "Machine Learning - ABC Platform\n"
        "SQL Certification - XYZ"
    ),
    height=120
)


# =====================================================
# ACHIEVEMENTS
# =====================================================

st.header(
    "⭐ Achievements"
)

achievements = st.text_area(
    "Achievements",
    placeholder=(
        "Winner - College Hackathon\n"
        "Participated in Coding Competition\n"
        "Presented project at Tech Fest"
    ),
    height=120
)


# =====================================================
# GENERATE
# =====================================================

st.divider()

if st.button(
    "📄 Generate Resume",
    use_container_width=True
):

    # ---------------------------------------------
    # VALIDATION
    # ---------------------------------------------

    if not name.strip():

        st.error(
            "❌ Please enter your full name."
        )

    elif not email.strip():

        st.error(
            "❌ Please enter your email."
        )

    else:

        # -----------------------------------------
        # CREATE PDF
        # -----------------------------------------

        pdf_file = create_resume_pdf(
            name=name,
            email=email,
            phone=phone,
            city=city,
            linkedin=linkedin,
            github=github,
            career_objective=career_objective,
            education=education,
            skills=skills,
            projects=projects,
            experience=experience,
            certifications=certifications,
            achievements=achievements
        )


        st.success(
            "✅ Resume created successfully!"
        )


        # -----------------------------------------
        # DOWNLOAD
        # -----------------------------------------

        st.download_button(
            label="⬇️ Download Resume PDF",
            data=pdf_file,
            file_name=f"{name.replace(' ', '_')}_Resume.pdf",
            mime="application/pdf",
            use_container_width=True
        )


# =====================================================
# TIPS
# =====================================================

st.divider()

st.info(
    """
💡 Resume Tips:

• Keep your resume simple and professional.
• Mention your technical skills clearly.
• Add projects with technologies used.
• Add certifications if available.
• Keep education information accurate.
• Add LinkedIn/GitHub if you have them.
• After downloading, upload the PDF in
  🤖 Job Recommendations to get skill-based
  job recommendations.
"""
)