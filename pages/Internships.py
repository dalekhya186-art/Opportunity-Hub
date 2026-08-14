import streamlit as st
import requests
import feedparser
from urllib.parse import quote

from auth import require_login
from ml.internship_recommend import predict_internship_score


# =====================================================
# LOGIN
# =====================================================

require_login()


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Internships",
    page_icon="💼",
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
# CITIES
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
    "Tirupati",
    "Tiruchirappalli",
    "Udaipur",
    "Vadodara",
    "Varanasi",
    "Vijayawada",
    "Visakhapatnam",
    "Warangal"

]


# =====================================================
# INTERNSHIP CATEGORIES
# =====================================================

CATEGORIES = [

    "All",

    "Software Development",
    "Web Development",
    "Data Science",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Analytics",
    "Cyber Security",
    "Cloud Computing",
    "Python",
    "Java",
    "Marketing",
    "Finance",
    "HR",
    "Business",
    "Mechanical",
    "Civil",
    "Electrical",
    "Electronics"

]


# =====================================================
# GET INTERNSHIPS
# =====================================================

def get_internships(
    city,
    category
):

    try:

        if city == "All India":

            location_text = "India"

        else:

            location_text = city


        if category == "All":

            search_text = (
                f"internship "
                f"{location_text} India 2026"
            )

        else:

            search_text = (
                f"{category} internship "
                f"{location_text} India 2026"
            )


        query = quote(
            search_text
        )


        url = (
            "https://news.google.com/rss/search?"
            f"q={query}"
            "&hl=en-IN"
            "&gl=IN"
            "&ceid=IN:en"
        )


        response = requests.get(
            url,
            timeout=15
        )


        response.raise_for_status()


        feed = feedparser.parse(
            response.content
        )


        return feed.entries


    except Exception:

        return []


# =====================================================
# CLEAN TITLE
# =====================================================

def clean_title(title):

    if " - " in title:

        return title.split(
            " - "
        )[0]

    return title


# =====================================================
# PAGE HEADER
# =====================================================

st.title(
    "💼 Internship Opportunities"
)

st.write(
    "Find new internship opportunities "
    "and get ML-based skill matching."
)

st.divider()


# =====================================================
# STUDENT SKILLS
# =====================================================

st.subheader(
    "🧑‍🎓 Your Skills"
)


# First try to get skills from session state
saved_skills = st.session_state.get(
    "student_skills",
    []
)


if saved_skills:

    student_skills = saved_skills

    st.success(
        "✅ Skills loaded from your profile/resume."
    )

    st.write(
        "🧠 Your Skills: "
        + ", ".join(student_skills)
    )

else:

    skills_input = st.text_input(
        "Enter your skills",
        placeholder=(
            "Example: Python, SQL, Machine Learning, AWS"
        )
    )


    if skills_input.strip():

        student_skills = [
            skill.strip()
            for skill in skills_input.split(",")
            if skill.strip()
        ]

        # Save for current session
        st.session_state[
            "student_skills"
        ] = student_skills

    else:

        student_skills = []


st.divider()


# =====================================================
# FILTERS
# =====================================================

col1, col2, col3 = st.columns(3)


with col1:

    selected_city = st.selectbox(
        "📍 Location",
        CITIES
    )


with col2:

    category = st.selectbox(
        "💻 Internship Category",
        CATEGORIES
    )


with col3:

    number = st.selectbox(
        "📋 Number of Updates",
        [10, 15, 20, 30]
    )


# =====================================================
# SEARCH
# =====================================================

if st.button(
    "🔎 Find New Internships",
    use_container_width=True
):


    if not student_skills:

        st.warning(
            "⚠️ Please enter your skills "
            "before searching internships."
        )

        st.stop()


    with st.spinner(
        "Searching internships and calculating ML scores..."
    ):

        results = get_internships(
            selected_city,
            category
        )


    if results:

        st.success(
            f"{len(results)} internship updates found."
        )


        # =================================================
        # CREATE ML SCORES
        # =================================================

        scored_results = []


        for item in results:

            title = clean_title(
                item.get(
                    "title",
                    "Internship Opportunity"
                )
            )


            summary = item.get(
                "summary",
                ""
            )


            link = item.get(
                "link",
                ""
            )


            published = item.get(
                "published",
                ""
            )


            # ---------------------------------------------
            # Internship text
            # ---------------------------------------------

            internship_text = (
                title
                + " "
                + summary
            )


            # ---------------------------------------------
            # ML prediction
            # ---------------------------------------------

            try:

                ml_result = predict_internship_score(
                    student_skills,
                    internship_text
                )

            except Exception as e:

                ml_result = {

                    "ml_score": 0,

                    "skill_match": 0,

                    "final_score": 0,

                    "matching_skills": []

                }


            scored_results.append({

                "title": title,

                "summary": summary,

                "link": link,

                "published": published,

                "ml_result": ml_result

            })


        # =================================================
        # SORT BY FINAL SCORE
        # =================================================

        scored_results.sort(
            key=lambda x:
                x["ml_result"]["final_score"],
            reverse=True
        )


        # =================================================
        # DISPLAY RESULTS
        # =================================================

        for item in scored_results[:number]:


            title = item["title"]

            summary = item["summary"]

            link = item["link"]

            published = item["published"]

            ml_result = item["ml_result"]


            with st.container(
                border=True
            ):


                st.subheader(
                    "💼 " + title
                )


                if published:

                    st.caption(
                        "🕒 " + published
                    )


                st.write(
                    "📍 Location: "
                    + selected_city
                )


                st.write(
                    "💻 Category: "
                    + category
                )


                # =================================================
                # ML SCORES
                # =================================================

                st.write(
                    f"🤖 **ML Score:** "
                    f"{ml_result['ml_score']}%"
                )


                st.write(
                    f"🎯 **Skill Match:** "
                    f"{ml_result['skill_match']}%"
                )


                st.write(
                    f"⭐ **Final Recommendation Score:** "
                    f"{ml_result['final_score']}%"
                )


                # =================================================
                # PROGRESS BAR
                # =================================================

                progress = (
                    ml_result["final_score"]
                    / 100
                )


                st.progress(
                    min(
                        max(
                            progress,
                            0.0
                        ),
                        1.0
                    )
                )


                # =================================================
                # MATCHING SKILLS
                # =================================================

                matching_skills = (
                    ml_result[
                        "matching_skills"
                    ]
                )


                if matching_skills:

                    st.write(
                        "🧠 **Matching Skills:** "
                        + ", ".join(
                            matching_skills
                        )
                    )

                else:

                    st.write(
                        "🧠 **Matching Skills:** "
                        "No matching skills detected"
                    )


                # =================================================
                # SUMMARY
                # =================================================

                if summary:

                    clean_summary = (
                        summary
                        .replace(
                            "<p>",
                            ""
                        )
                        .replace(
                            "</p>",
                            ""
                        )
                    )


                    st.write(
                        clean_summary[:400]
                    )


                # =================================================
                # APPLY
                # =================================================

                if link:

                    st.link_button(
                        "🚀 View Details / Apply",
                        link,
                        use_container_width=True
                    )


    else:

        st.warning(
            "No internship updates found "
            "for this selection."
        )


# =====================================================
# INTERNSHIP PORTALS
# =====================================================

st.divider()

st.subheader(
    "🌐 Internship Search Portals"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        "**💼 Internshala**"
    )

    st.link_button(
        "Find Internships",
        "https://internshala.com/internships/",
        use_container_width=True
    )


with col2:

    st.markdown(
        "**💻 LinkedIn Jobs**"
    )

    st.link_button(
        "Find Internships",
        "https://www.linkedin.com/jobs/",
        use_container_width=True
    )


with col3:

    st.markdown(
        "**🔎 Google Jobs Search**"
    )

    search_url = (
        "https://www.google.com/search?"
        "q=internships+India+2026"
    )


    st.link_button(
        "Search",
        search_url,
        use_container_width=True
    )
