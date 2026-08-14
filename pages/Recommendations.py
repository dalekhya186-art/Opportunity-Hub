import streamlit as st
from urllib.parse import quote

from pypdf import PdfReader
from docx import Document

from ml.recommendation_train import predict_match_score
from auth import require_login


# =====================================================
# LOGIN
# =====================================================

require_login()


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Job Recommendations",
    page_icon="🤖",
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
# INDIAN CITIES
# =====================================================

CITIES = [

    "All India",

    "Ahmedabad",
    "Bengaluru",
    "Bhopal",
    "Bhubaneswar",
    "Chandigarh",
    "Chennai",
    "Coimbatore",
    "Delhi",
    "Faridabad",
    "Ghaziabad",
    "Gurugram",
    "Guwahati",
    "Hyderabad",
    "Indore",
    "Jaipur",
    "Jamshedpur",
    "Kanpur",
    "Kochi",
    "Kolkata",
    "Lucknow",
    "Ludhiana",
    "Madurai",
    "Mangaluru",
    "Mohali",
    "Mumbai",
    "Mysuru",
    "Nagpur",
    "Nashik",
    "Noida",
    "Patna",
    "Pune",
    "Raipur",
    "Rajkot",
    "Ranchi",
    "Surat",
    "Thiruvananthapuram",
    "Tiruchirappalli",
    "Udaipur",
    "Vadodara",
    "Varanasi",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal"

]


# =====================================================
# SUPPORTED SKILLS
# =====================================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "html",
    "css",
    "react",
    "angular",
    "node",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",

    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",

    "power bi",
    "tableau",
    "excel",

    "aws",
    "azure",
    "google cloud",

    "docker",
    "kubernetes",

    "git",
    "github",

    "linux"

]


# =====================================================
# COMPANIES
# =====================================================

COMPANIES = [

    {
        "name": "TCS",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mumbai",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.tcs.com/careers"
    },

    {
        "name": "Infosys",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mysuru"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.infosys.com/careers/"
    },

    {
        "name": "Wipro",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://careers.wipro.com/"
    },

    {
        "name": "Accenture",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Mumbai",
            "Noida"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.accenture.com/in-en/careers"
    },

    {
        "name": "HCLTech",
        "cities": [
            "Noida",
            "Chennai",
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Lucknow"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://www.hcltech.com/careers"
    },

    {
        "name": "Tech Mahindra",
        "cities": [
            "Pune",
            "Hyderabad",
            "Bengaluru",
            "Chennai",
            "Noida",
            "Mumbai"
        ],
        "skills": [
            "python",
            "java",
            "sql",
            "javascript",
            "cloud"
        ],
        "url": "https://careers.techmahindra.com/"
    },

    {
        "name": "Oracle",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Pune",
            "Noida"
        ],
        "skills": [
            "java",
            "python",
            "sql",
            "cloud",
            "database"
        ],
        "url": "https://www.oracle.com/careers/"
    },

    {
        "name": "Salesforce",
        "cities": [
            "Bengaluru",
            "Hyderabad",
            "Mumbai"
        ],
        "skills": [
            "javascript",
            "python",
            "sql",
            "cloud"
        ],
        "url": "https://www.salesforce.com/company/careers/"
    }

]


# =====================================================
# PDF READER
# =====================================================

def read_pdf(file):

    try:

        reader = PdfReader(file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted + "\n"

        return text

    except Exception:

        return ""


# =====================================================
# DOCX READER
# =====================================================

def read_docx(file):

    try:

        document = Document(file)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text

    except Exception:

        return ""


# =====================================================
# RESUME READER
# =====================================================

def extract_resume(file):

    filename = file.name.lower()

    if filename.endswith(".pdf"):

        return read_pdf(file)

    if filename.endswith(".docx"):

        return read_docx(file)

    return ""


# =====================================================
# SKILL DETECTOR
# =====================================================

def find_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:

        if skill in text:

            detected.append(skill)

    return list(
        dict.fromkeys(detected)
    )


# =====================================================
# JOB SEARCH URL
# =====================================================

def create_job_search_url(
    skill,
    city
):

    query = quote(
        f"{skill} jobs {city} India"
    )

    return (
        "https://www.google.com/search?"
        f"q={query}"
    )


# =====================================================
# PAGE HEADER
# =====================================================

st.title(
    "🤖 Resume Based Job Recommendations"
)

st.write(
    "Upload your resume, select a city and "
    "find job opportunities matching your skills."
)

st.divider()


# =====================================================
# CITY
# =====================================================

selected_city = st.selectbox(
    "📍 Select Job Location",
    CITIES
)


st.info(
    f"Searching opportunities for: {selected_city}"
)


# =====================================================
# RESUME UPLOAD
# =====================================================

resume = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf", "docx"]
)


# =====================================================
# ANALYSIS
# =====================================================

if resume:

    st.success(
        f"Uploaded: {resume.name}"
    )


    if st.button(
        "🤖 Analyze Resume & Recommend Jobs",
        use_container_width=True
    ):

        # ---------------------------------------------
        # READ RESUME
        # ---------------------------------------------

        with st.spinner(
            "Analyzing your resume..."
        ):

            resume_text = extract_resume(
                resume
            )


        # ---------------------------------------------
        # RESUME CHECK
        # ---------------------------------------------

        if not resume_text.strip():

            st.error(
                "Could not read this resume. "
                "Please upload a text-based PDF or DOCX."
            )

            st.stop()


        # ---------------------------------------------
        # DETECT SKILLS
        # ---------------------------------------------

        detected_skills = find_skills(
            resume_text
        )


        # ---------------------------------------------
        # ML PREDICTION
        # ---------------------------------------------

        try:

            ml_score = predict_match_score(
                detected_skills
            )

        except Exception as e:

            st.error(
                "Unable to run the ML recommendation model."
            )

            st.exception(e)

            st.stop()


        # =================================================
        # DETECTED SKILLS
        # =================================================

        st.subheader(
            "🧠 Skills Detected"
        )


        if detected_skills:

            st.success(
                ", ".join(
                    skill.title()
                    for skill in detected_skills
                )
            )

        else:

            st.warning(
                "No supported skills were detected."
            )

            st.info(
                "Add skills such as Python, Java, SQL, "
                "Machine Learning, AWS, Excel etc."
            )


        # =================================================
        # ML SCORE
        # =================================================

        st.divider()

        st.subheader(
            "🤖 ML Recommendation Score"
        )

        st.metric(
            "Predicted Skill Match",
            f"{ml_score}%"
        )

        st.progress(
            min(
                int(ml_score),
                100
            )
        )

        st.caption(
            "This score is generated by the trained "
            "Random Forest recommendation model."
        )


        # =================================================
        # COMPANY MATCHING
        # =================================================

        st.divider()

        st.subheader(
            "🏢 Recommended Companies"
        )


        matches = []


        for company in COMPANIES:

            company_cities = company["cities"]


            # ---------------------------------------------
            # CITY FILTER
            # ---------------------------------------------

            if selected_city != "All India":

                if selected_city not in company_cities:

                    continue


            # ---------------------------------------------
            # SKILL MATCH
            # ---------------------------------------------

            matched_skills = []


            for skill in detected_skills:

                company_skills = [
                    item.lower()
                    for item in company["skills"]
                ]


                if skill.lower() in company_skills:

                    matched_skills.append(
                        skill
                    )


            # ---------------------------------------------
            # COMPANY SCORE
            # ---------------------------------------------

            if matched_skills:

                if detected_skills:

                    company_score = (
                        len(matched_skills)
                        /
                        len(detected_skills)
                    ) * 100

                else:

                    company_score = 0


                # Combine company skill score
                # with ML score

                final_score = (
                    company_score * 0.6
                    +
                    ml_score * 0.4
                )


                matches.append(
                    (
                        company,
                        matched_skills,
                        company_score,
                        final_score
                    )
                )


        # =================================================
        # SORT
        # =================================================

        matches.sort(
            key=lambda x: x[3],
            reverse=True
        )


        # =================================================
        # DISPLAY COMPANIES
        # =================================================

        if matches:

            st.success(
                f"{len(matches)} companies matched your profile."
            )


            for (
                company,
                matched,
                company_score,
                final_score
            ) in matches:


                with st.container(
                    border=True
                ):

                    st.subheader(
                        "🏢 "
                        +
                        company["name"]
                    )


                    st.write(
                        "📍 Available cities: "
                        +
                        ", ".join(
                            company["cities"]
                        )
                    )


                    st.write(
                        f"🤖 ML Score: {ml_score:.1f}%"
                    )


                    st.write(
                        f"🎯 Company Skill Match: "
                        f"{company_score:.1f}%"
                    )


                    st.write(
                        f"⭐ Final Recommendation Score: "
                        f"{final_score:.1f}%"
                    )


                    st.progress(
                        min(
                            int(final_score),
                            100
                        )
                    )


                    st.write(
                        "🧠 Matching Skills: "
                        +
                        ", ".join(
                            matched
                        )
                    )


                    st.link_button(
                        "🚀 Company Careers / Apply",
                        company["url"],
                        use_container_width=True
                    )


        else:

            st.warning(
                "No company matched your detected skills "
                "for the selected city."
            )


        # =================================================
        # JOB SEARCH
        # =================================================

        st.divider()

        st.subheader(
            "🔎 Search Jobs For Your Skills"
        )


        if detected_skills:

            for skill in detected_skills[:10]:

                if selected_city == "All India":

                    search_city = "India"

                else:

                    search_city = selected_city


                url = create_job_search_url(
                    skill,
                    search_city
                )


                st.link_button(
                    f"🔎 {skill.title()} Jobs - {search_city}",
                    url,
                    use_container_width=True
                )


        else:

            st.info(
                "Skills are required to generate job searches."
            )
