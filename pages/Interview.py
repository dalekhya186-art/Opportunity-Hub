import streamlit as st
import re
import sys
import random
from pathlib import Path


# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# =====================================================
# LOGIN
# =====================================================

from auth import require_login

require_login()


# =====================================================
# ML INTERVIEW MODEL
# =====================================================

from  ml.interview_recommend import (
    evaluate_answer as ml_evaluate_answer
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Interview Preparation",
    page_icon="🎤",
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

st.sidebar.page_link(
    "pages/Interview.py",
    label="🎤 Interview Preparation"
)


# =====================================================
# QUESTION BANK
# =====================================================

QUESTION_BANK = {

    "Python Developer": {

        "Technical": [

            {
                "question":
                    "What is Python and what are its main advantages?",

                "expected_answer":
                    (
                        "Python is a high level interpreted "
                        "programming language. It is dynamically "
                        "typed, readable, easy to use and supports "
                        "object oriented programming."
                    ),

                "keywords": [
                    "interpreted",
                    "high level",
                    "dynamic",
                    "object oriented",
                    "readable"
                ]
            },

            {
                "question":
                    "What is the difference between a list and a tuple in Python?",

                "expected_answer":
                    (
                        "A list is mutable while a tuple is immutable. "
                        "Lists can be changed after creation whereas "
                        "tuples cannot be changed."
                    ),

                "keywords": [
                    "list",
                    "tuple",
                    "mutable",
                    "immutable"
                ]
            },

            {
                "question":
                    "What is a dictionary in Python?",

                "expected_answer":
                    (
                        "A dictionary is a data structure that stores "
                        "data as key value pairs. Each key is used to "
                        "access its corresponding value."
                    ),

                "keywords": [
                    "key",
                    "value",
                    "key value",
                    "mapping"
                ]
            },

            {
                "question":
                    "What is exception handling in Python?",

                "expected_answer":
                    (
                        "Exception handling is used to handle runtime "
                        "errors using try, except and finally blocks."
                    ),

                "keywords": [
                    "try",
                    "except",
                    "finally",
                    "error"
                ]
            },

            {
                "question":
                    "What is object-oriented programming?",

                "expected_answer":
                    (
                        "Object oriented programming is a programming "
                        "paradigm based on classes and objects. It "
                        "supports concepts such as inheritance, "
                        "polymorphism and encapsulation."
                    ),

                "keywords": [
                    "class",
                    "object",
                    "inheritance",
                    "polymorphism",
                    "encapsulation"
                ]
            },

            {
                "question":
                    "What is the difference between == and is in Python?",

                "expected_answer":
                    (
                        "The == operator compares values while the is "
                        "operator checks whether two objects have the "
                        "same identity in memory."
                    ),

                "keywords": [
                    "value",
                    "identity",
                    "memory"
                ]
            }
        ],

        "HR": [

            {
                "question":
                    "Tell me about yourself.",

                "expected_answer":
                    (
                        "I am a student with relevant education and "
                        "technical skills. I have worked on projects "
                        "and I want to improve my skills and build "
                        "my career."
                    ),

                "keywords": [
                    "education",
                    "skills",
                    "project",
                    "experience",
                    "goal"
                ]
            },

            {
                "question":
                    "Why do you want to become a Python Developer?",

                "expected_answer":
                    (
                        "I am interested in Python development because "
                        "Python is easy to learn and useful for software "
                        "development, automation and problem solving."
                    ),

                "keywords": [
                    "python",
                    "development",
                    "problem solving",
                    "career"
                ]
            },

            {
                "question":
                    "What are your strengths?",

                "expected_answer":
                    (
                        "My strengths include problem solving, "
                        "communication, continuous learning and "
                        "teamwork."
                    ),

                "keywords": [
                    "problem solving",
                    "communication",
                    "learning",
                    "teamwork"
                ]
            },

            {
                "question":
                    "Where do you see yourself in five years?",

                "expected_answer":
                    (
                        "In five years I want to have strong technical "
                        "skills, grow professionally and become an "
                        "experienced developer."
                    ),

                "keywords": [
                    "career",
                    "skills",
                    "growth",
                    "developer"
                ]
            }
        ]
    },


    "Data Scientist": {

        "Technical": [

            {
                "question":
                    "What is the difference between supervised and unsupervised learning?",

                "expected_answer":
                    (
                        "Supervised learning uses labelled data for "
                        "training while unsupervised learning uses "
                        "unlabelled data. Classification is an example "
                        "of supervised learning and clustering is an "
                        "example of unsupervised learning."
                    ),

                "keywords": [
                    "supervised",
                    "unsupervised",
                    "labelled",
                    "unlabelled",
                    "classification",
                    "clustering"
                ]
            },

            {
                "question":
                    "What is overfitting in machine learning?",

                "expected_answer":
                    (
                        "Overfitting happens when a model performs very "
                        "well on training data but performs poorly on "
                        "unseen test data because the model has learned "
                        "the training data too closely."
                    ),

                "keywords": [
                    "training",
                    "test",
                    "generalization",
                    "complex",
                    "performance"
                ]
            },

            {
                "question":
                    "What is the difference between classification and regression?",

                "expected_answer":
                    (
                        "Classification predicts categorical values "
                        "while regression predicts continuous numerical "
                        "values."
                    ),

                "keywords": [
                    "classification",
                    "regression",
                    "categorical",
                    "continuous",
                    "prediction"
                ]
            },

            {
                "question":
                    "What is feature engineering?",

                "expected_answer":
                    (
                        "Feature engineering is the process of creating "
                        "or transforming features from raw data to "
                        "improve machine learning model performance."
                    ),

                "keywords": [
                    "features",
                    "data",
                    "transformation",
                    "model",
                    "performance"
                ]
            },

            {
                "question":
                    "What is a confusion matrix?",

                "expected_answer":
                    (
                        "A confusion matrix is used to evaluate a "
                        "classification model using true positive, "
                        "true negative, false positive and false "
                        "negative predictions."
                    ),

                "keywords": [
                    "true positive",
                    "true negative",
                    "false positive",
                    "false negative"
                ]
            },

            {
                "question":
                    "Why do we split data into training and testing sets?",

                "expected_answer":
                    (
                        "We split data into training and testing sets "
                        "so that the model can learn from training data "
                        "and be evaluated on unseen data."
                    ),

                "keywords": [
                    "training",
                    "testing",
                    "unseen",
                    "evaluation",
                    "generalization"
                ]
            }
        ],

        "HR": [

            {
                "question":
                    "Tell me about yourself.",

                "expected_answer":
                    (
                        "I have a background in data science and "
                        "machine learning. I have technical skills "
                        "and project experience and I want to grow "
                        "my career."
                    ),

                "keywords": [
                    "education",
                    "skills",
                    "project",
                    "experience",
                    "goal"
                ]
            },

            {
                "question":
                    "Why do you want to become a Data Scientist?",

                "expected_answer":
                    (
                        "I am interested in data science because I "
                        "enjoy working with data, analysis, machine "
                        "learning and solving real world problems."
                    ),

                "keywords": [
                    "data",
                    "analysis",
                    "machine learning",
                    "problem solving",
                    "career"
                ]
            },

            {
                "question":
                    "Describe a data science project you have worked on.",

                "expected_answer":
                    (
                        "I worked on a project where I identified a "
                        "problem, collected and prepared data, trained "
                        "a model and evaluated the results."
                    ),

                "keywords": [
                    "problem",
                    "data",
                    "model",
                    "result",
                    "project"
                ]
            },

            {
                "question":
                    "How do you handle a difficult problem?",

                "expected_answer":
                    (
                        "I analyze the problem, research possible "
                        "solutions, test different approaches and "
                        "learn from the results."
                    ),

                "keywords": [
                    "analysis",
                    "research",
                    "solution",
                    "learning"
                ]
            }
        ]
    },


    "Machine Learning Engineer": {

        "Technical": [

            {
                "question":
                    "What is machine learning?",

                "expected_answer":
                    (
                        "Machine learning is a field of artificial "
                        "intelligence where algorithms learn patterns "
                        "from data to make predictions or decisions."
                    ),

                "keywords": [
                    "data",
                    "model",
                    "learning",
                    "prediction",
                    "algorithm"
                ]
            },

            {
                "question":
                    "What is the difference between training and testing data?",

                "expected_answer":
                    (
                        "Training data is used to train the machine "
                        "learning model while testing data is unseen "
                        "data used to evaluate the model."
                    ),

                "keywords": [
                    "training",
                    "testing",
                    "unseen",
                    "evaluation"
                ]
            },

            {
                "question":
                    "What is cross-validation?",

                "expected_answer":
                    (
                        "Cross-validation is a technique that divides "
                        "data into multiple folds and uses different "
                        "folds for training and validation to evaluate "
                        "model performance."
                    ),

                "keywords": [
                    "validation",
                    "fold",
                    "training",
                    "testing",
                    "evaluation"
                ]
            },

            {
                "question":
                    "What is regularization?",

                "expected_answer":
                    (
                        "Regularization is a technique used to reduce "
                        "overfitting by adding a penalty to the model. "
                        "L1 and L2 are common types of regularization."
                    ),

                "keywords": [
                    "overfitting",
                    "l1",
                    "l2",
                    "penalty",
                    "model"
                ]
            },

            {
                "question":
                    "What is the purpose of feature scaling?",

                "expected_answer":
                    (
                        "Feature scaling puts numerical features on a "
                        "similar scale using methods such as normalization "
                        "or standardization."
                    ),

                "keywords": [
                    "scale",
                    "features",
                    "normalization",
                    "standardization"
                ]
            }
        ],

        "HR": [

            {
                "question":
                    "Tell me about yourself.",

                "expected_answer":
                    (
                        "I have relevant education and technical skills "
                        "in machine learning. I have worked on projects "
                        "and want to grow as an ML engineer."
                    ),

                "keywords": [
                    "education",
                    "skills",
                    "project",
                    "experience"
                ]
            },

            {
                "question":
                    "Why are you interested in Machine Learning?",

                "expected_answer":
                    (
                        "I am interested in machine learning because "
                        "it combines data, algorithms and problem solving "
                        "to build useful predictive systems."
                    ),

                "keywords": [
                    "machine learning",
                    "data",
                    "problem solving",
                    "career"
                ]
            },

            {
                "question":
                    "Tell me about an ML project you worked on.",

                "expected_answer":
                    (
                        "I worked on an ML project where I defined a "
                        "problem, collected a dataset, trained a model "
                        "and evaluated the result."
                    ),

                "keywords": [
                    "problem",
                    "dataset",
                    "model",
                    "result",
                    "project"
                ]
            }
        ]
    },


    "Web Developer": {

        "Technical": [

            {
                "question":
                    "What is HTML?",

                "expected_answer":
                    (
                        "HTML is a markup language used to create the "
                        "structure and elements of web pages."
                    ),

                "keywords": [
                    "markup",
                    "structure",
                    "web",
                    "elements"
                ]
            },

            {
                "question":
                    "What is CSS used for?",

                "expected_answer":
                    (
                        "CSS is used to style web pages and control "
                        "their design, layout and appearance."
                    ),

                "keywords": [
                    "style",
                    "design",
                    "layout",
                    "web"
                ]
            },

            {
                "question":
                    "What is JavaScript?",

                "expected_answer":
                    (
                        "JavaScript is a programming language used to "
                        "make web pages interactive and dynamic."
                    ),

                "keywords": [
                    "programming",
                    "web",
                    "interactive",
                    "browser"
                ]
            },

            {
                "question":
                    "What is the difference between frontend and backend?",

                "expected_answer":
                    (
                        "Frontend is the user interface that users "
                        "interact with. Backend runs on the server and "
                        "handles application logic and databases."
                    ),

                "keywords": [
                    "frontend",
                    "backend",
                    "user interface",
                    "server",
                    "database"
                ]
            }
        ],

        "HR": [

            {
                "question":
                    "Tell me about yourself.",

                "expected_answer":
                    (
                        "I have relevant education, technical skills "
                        "and project experience in web development."
                    ),

                "keywords": [
                    "education",
                    "skills",
                    "project",
                    "experience"
                ]
            },

            {
                "question":
                    "Why do you want to become a Web Developer?",

                "expected_answer":
                    (
                        "I am interested in web development because "
                        "I enjoy building websites, working with design "
                        "and solving development problems."
                    ),

                "keywords": [
                    "web",
                    "development",
                    "design",
                    "career"
                ]
            },

            {
                "question":
                    "Describe one web project you have built.",

                "expected_answer":
                    (
                        "I built a web project involving frontend "
                        "development, backend logic and a database. "
                        "The project solved a specific problem."
                    ),

                "keywords": [
                    "project",
                    "frontend",
                    "backend",
                    "database",
                    "result"
                ]
            }
        ]
    }
}


# =====================================================
# SESSION STATE
# =====================================================

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "questions" not in st.session_state:
    st.session_state.questions = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "interview_completed" not in st.session_state:
    st.session_state.interview_completed = False

if "interview_role" not in st.session_state:
    st.session_state.interview_role = ""

if "interview_type" not in st.session_state:
    st.session_state.interview_type = ""


# =====================================================
# FEATURE CALCULATION
# =====================================================

def calculate_interview_features(
    answer,
    keywords,
    expected_answer
):

    answer_lower = answer.lower()

    matched = [
        kw
        for kw in keywords
        if kw.lower() in answer_lower
    ]

    keyword_match = (
        len(matched) / len(keywords)
        if keywords
        else 0.0
    )

    answer_length = len(
        answer.split()
    )

    technical_terms = len(
        matched
    )

    expected_words = set(
        expected_answer.lower().split()
    )

    answer_words = set(
        answer_lower.split()
    )

    answer_similarity = (
        len(
            expected_words.intersection(
                answer_words
            )
        )
        / len(expected_words)
        if expected_words
        else 0.0
    )

    return (
        keyword_match,
        answer_similarity,
        answer_length,
        technical_terms,
        matched
    )


# =====================================================
# PAGE HEADER
# =====================================================

st.title("🎤 Interview Preparation")

st.write(
    "Practice technical and HR interview questions "
    "using an ML-based answer evaluation system."
)

st.divider()


# =====================================================
# INTERVIEW SETUP
# =====================================================

if not st.session_state.interview_started:

    role = st.selectbox(
        "🎯 Select Target Role",
        list(QUESTION_BANK.keys())
    )

    interview_type = st.selectbox(
        "📚 Interview Type",
        ["Technical"]
    )

    number = st.selectbox(
        "📋 Number of Questions",
        [1, 3]
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        available_questions = (
            QUESTION_BANK[
                role
            ][
                interview_type
            ]
        )

        selected_questions = random.sample(
            available_questions,
            min(
                number,
                len(available_questions)
            )
        )

        st.session_state.questions = (
            selected_questions
        )

        st.session_state.interview_role = (
            role
        )

        st.session_state.interview_type = (
            interview_type
        )

        st.session_state.current_question = 0

        st.session_state.scores = []

        st.session_state.interview_started = True

        st.session_state.interview_completed = False

        st.rerun()


# =====================================================
# INTERVIEW IN PROGRESS
# =====================================================

elif (
    st.session_state.interview_started
    and not st.session_state.interview_completed
):

    total = len(
        st.session_state.questions
    )

    current = (
        st.session_state.current_question
    )

    question_data = (
        st.session_state.questions[
            current
        ]
    )

    st.subheader(
        f"Question {current + 1} of {total}"
    )

    st.write(
        f"❓ {question_data['question']}"
    )

    answer = st.text_area(
        "✍️ Type your answer",
        key=f"answer_{current}"
    )


    # =================================================
    # SUBMIT ANSWER
    # =================================================

    if st.button(
        "✅ Submit Answer",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning(
                "⚠️ Please type an answer before submitting."
            )

        else:

            (
                keyword_match,
                answer_similarity,
                answer_length,
                technical_terms,
                matched
            ) = calculate_interview_features(
                answer,
                question_data["keywords"],
                question_data["expected_answer"]
            )


            # -----------------------------------------
            # ML MODEL
            # -----------------------------------------

            result = ml_evaluate_answer(

                st.session_state.interview_role,

                st.session_state.interview_type,

                question_data["question"],

                question_data["expected_answer"],

                answer,

                keyword_match,

                answer_similarity,

                answer_length,

                technical_terms
            )


            # -----------------------------------------
            # SAVE SCORE
            # -----------------------------------------

            # Prevent duplicate score for same question
            if len(
                st.session_state.scores
            ) <= current:

                st.session_state.scores.append(
                    result
                )

            else:

                st.session_state.scores[current] = (
                    result
                )


            # -----------------------------------------
            # DISPLAY RESULT
            # -----------------------------------------

            st.success(
                f"🎯 Predicted Score: {result}/10"
            )

            st.write(
                f"🔑 Keyword Match: "
                f"{keyword_match:.2f}"
            )

            st.write(
                f"📚 Answer Similarity: "
                f"{answer_similarity:.2f}"
            )

            st.write(
                f"📝 Answer Length: "
                f"{answer_length} words"
            )

            st.write(
                f"💡 Technical Terms: "
                f"{technical_terms}"
            )


    # =================================================
    # NEXT QUESTION
    # =================================================

    if st.button(
        "➡️ Next Question",
        use_container_width=True
    ):

        st.session_state.current_question += 1

        if (
            st.session_state.current_question
            >= total
        ):

            st.session_state.interview_completed = True

        st.rerun()


# =====================================================
# REVIEW PAGE
# =====================================================

elif st.session_state.interview_completed:

    st.subheader(
        "🎉 Interview Completed!"
    )

    # -------------------------------------------------
    # AVERAGE SCORE
    # -------------------------------------------------

    if len(
        st.session_state.scores
    ) > 0:

        avg_score = (
            sum(
                st.session_state.scores
            )
            /
            len(
                st.session_state.scores
            )
        )

        st.success(
            f"✅ Average Score: "
            f"{avg_score:.2f}/10"
        )

    else:

        st.warning(
            "⚠️ No answers were submitted."
        )


    # -------------------------------------------------
    # REVIEW
    # -------------------------------------------------

    st.write(
        "📝 Review of your answers:"
    )

    for i, q in enumerate(
        st.session_state.questions
    ):

        st.write(
            f"### Q{i + 1}: "
            f"{q['question']}"
        )

        if (
            i
            <
            len(
                st.session_state.scores
            )
        ):

            st.write(
                f"🎯 Score: "
                f"{st.session_state.scores[i]}/10"
            )

        else:

            st.write(
                "Score: Not submitted ❌"
            )


    # -------------------------------------------------
    # NEW INTERVIEW
    # -------------------------------------------------

    if st.button(
        "🔄 Start New Interview",
        use_container_width=True
    ):

        st.session_state.interview_started = False

        st.session_state.current_question = 0

        st.session_state.questions = []

        st.session_state.scores = []

        st.session_state.interview_completed = False

        st.session_state.interview_role = ""

        st.session_state.interview_type = ""

        st.rerun()
