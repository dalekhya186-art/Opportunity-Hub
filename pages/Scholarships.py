import streamlit as st
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime


from auth import require_login
from ml.scholarship_recommend import predict_scholarship_score


require_login()
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Scholarships",
    page_icon="🎓",
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
# SCHOLARSHIP CATEGORIES
# =====================================================

CATEGORIES = [

    "All",
    "Engineering",
    "Computer Science",
    "Medical",
    "MBA",
    "Arts",
    "Science",
    "Government",
    "Private",
    "Women",
    "Merit",
    "Need Based",
    "International"

]


# =====================================================
# SEARCH SCHOLARSHIPS
# =====================================================

def get_scholarships(category):

    try:

        if category == "All":

            search_text = (
                "scholarship India students 2026"
            )

        else:

            search_text = (
                f"{category} scholarship India 2026"
            )


        query = quote(search_text)


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


    except Exception as e:

        st.error(
            "Unable to fetch scholarship updates."
        )

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
    "🎓 Scholarship Opportunities"
)

st.write(
    "Find new scholarship updates available "
    "for students across India."
)

st.divider()


# =====================================================
# FILTERS
# =====================================================

col1, col2 = st.columns(2)


with col1:

    category = st.selectbox(
        "📚 Scholarship Category",
        CATEGORIES
    )


with col2:

    limit = st.selectbox(
        "📋 Number of Updates",
        [10, 15, 20, 30]
    )


# =====================================================
# SEARCH BUTTON
# =====================================================

if st.button(
    "🔎 Check New Scholarship Updates",
    use_container_width=True
):


    with st.spinner(
        "Finding latest scholarships..."
    ):


        results = get_scholarships(
            category
        )


    if results:

        st.success(
            f"{len(results)} updates found."
        )


        # =================================================
        # DISPLAY
        # =================================================

        for item in results[:limit]:


            title = clean_title(
                item.get(
                    "title",
                    "Scholarship Opportunity"
                )
            )


            link = item.get(
                "link",
                ""
            )


            published = item.get(
                "published",
                ""
            )


            summary = item.get(
                "summary",
                ""
            )


            with st.container(
                border=True
            ):


                st.subheader(
                    "🎓 " + title
                )


                if published:

                    st.caption(
                        "🕒 " + published
                    )


                st.write(
                    "🇮🇳 Location: India"
                )


                st.write(
                    "📚 Category: "
                    + category
                )


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


                if link:

                    st.link_button(
                        "🚀 View Details / Apply",
                        link,
                        use_container_width=True
                    )


    else:

        st.warning(
            "No scholarship updates found."
        )


# =====================================================
# IMPORTANT SOURCES
# =====================================================

st.divider()

st.subheader(
    "🌐 Important Scholarship Portals"
)

portal1, portal2, portal3 = st.columns(3)


with portal1:

    st.markdown(
        "**🎓 National Scholarship Portal**"
    )

    st.link_button(
        "Open Portal",
        "https://scholarships.gov.in/",
        use_container_width=True
    )


with portal2:

    st.markdown(
        "**🏛️ Government Scholarships**"
    )

    st.link_button(
        "Open Portal",
        "https://www.india.gov.in/",
        use_container_width=True
    )


with portal3:

    st.markdown(
        "**📚 Education Updates**"
    )

    st.link_button(
        "Search Scholarships",
        "https://www.google.com/search?q=India+scholarships+2026",
        use_container_width=True
    )