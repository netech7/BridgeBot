import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
from ingest import process_documents
from utils.qa import get_answer_with_sources
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from utils.decrypt_key import get_decrypted_api_key

# --- Page Configuration ---
st.set_page_config(page_title="BridgeAI: Smart Information Assistant", layout="wide")

# --- Login/Authentication ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    with st.form("Login"):
        st.subheader("🔒 Please log in to access BridgeAI")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            if username == "admin" and password == "bridge2025":
                st.session_state.authenticated = True
                st.success("🔓 Login successful!")
            else:
                st.error("❌ Invalid credentials. Try again.")

if not st.session_state.authenticated:
    login()
    st.stop()

# --- Logout Button ---
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# --- Custom Styling with Transitions ---
st.markdown("""
    <style>
    .main {
        background-color: #0A2F35;
        transition: background-color 0.4s ease;
    }
    .stButton button, .stDownloadButton button {
        background-color: #4A90E2;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1.5em;
        transition: all 0.3s ease;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        background-color: #1C6DD0;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input, .stChatInput input {
        border-radius: 8px;
        background-color: #E3F2F3;
        color: black;
        transition: background-color 0.3s;
    }
    .stFileUploader {
        border: 2px dashed #4A90E2;
        background-color: #DFEBEB;
        border-radius: 10px;
        padding: 10px;
        transition: all 0.3s ease;
    }
    .stFileUploader:hover {
        background-color: #D0E9EA;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- Prescriptive Trigger Function ---
def get_prescriptive_suggestion(user_query):
    triggers = [
        {
            "keywords": ["vendor", "data", "leak"],
            "suggestion": "💡 Would you like to initiate a vendor risk reassessment?",
            "action": "Initiate Risk Review"
        },
        {
            "keywords": ["gdpr", "privacy"],
            "suggestion": "💡 Do you want to notify the Data Privacy Officer?",
            "action": "Notify DPO"
        }
    ]
    for t in triggers:
        if all(word in user_query.lower() for word in t["keywords"]):
            return t["suggestion"], t["action"]
    return None, None

# --- Header ---
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<h1 style= 'padding-top: 17px;'> </h1>", unsafe_allow_html=True)
    st.image("bsid.png", width=170)
with col2:
    st.markdown("<h1 style='color:#FD8A8A; padding-top: 10px;'>Bridge InfoSys: Smart Information Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color:white;'>
        A user-friendly, AI-powered assistant that helps retrieve document-specific policies instantly using natural language queries.\n
        BridgeAI helps you instantly understand, analyze, and interact with your internal documents using AI.
        Upload files and ask questions to retrieve key insights effortlessly.
        </p>
    """, unsafe_allow_html=True)

# --- Session State ---
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# --- Upload Section ---
with st.expander("📂 Upload Documents", expanded=True):
    uploaded_files = st.file_uploader(
        "Supported formats: PDF, Word, Excel, PowerPoint, Images",
        type=["pdf", "docx", "xlsx", "pptx", "png", "jpeg", "jpg"],
        accept_multiple_files=True,
        help="You can upload multiple documents here."
    )

# --- Process and Embed ---
if uploaded_files:
    with st.spinner("🔍 Processing documents... Please wait."):
        gemini_api_key = get_decrypted_api_key()
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        docs = process_documents(uploaded_files, embedding_model)
        db = FAISS.from_documents(docs, embedding_model)
    st.success("✅ Documents processed and indexed successfully!")

    # --- Visuals for Excel Files ---
    for file in uploaded_files:
        if file.name.endswith(".xlsx"):
            try:
                st.markdown(f"<h6 style='color:white; margin-top: 2px; margin-bottom: 2px;'>📊 Data Preview: `{file.name}`</h6>", unsafe_allow_html=True)
                df = pd.read_excel(file)
                st.dataframe(df, use_container_width=True)

                with st.container():
                    st.markdown("<div style='margin-top:-25px; padding: 0px 10px;'>", unsafe_allow_html=True)

                st.markdown("<h6 style='color:white;margin-top: 2px; margin-bottom: 2px;'>📈 Auto Chart Preview</h6>", unsafe_allow_html=True)
                numeric_cols = df.select_dtypes(include='number').columns.tolist()
                if len(numeric_cols) >= 2:
                    x_axis = st.selectbox("Select X-axis", options=numeric_cols, key=file.name+"_x")
                    y_axis = st.selectbox("Select Y-axis", options=numeric_cols, key=file.name+"_y")
                    chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"], key=file.name+"_chart")
                    fig, ax = plt.subplots(figsize=(4.5, 2.8), tight_layout=True)
                    if chart_type == "Line":
                        df.plot(kind='line', x=x_axis, y=y_axis, ax=ax)
                    elif chart_type == "Bar":
                        df.plot(kind='bar', x=x_axis, y=y_axis, ax=ax)
                    elif chart_type == "Scatter":
                        df.plot(kind='scatter', x=x_axis, y=y_axis, ax=ax)
                    st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not render Excel content: {e}")

    # --- Q&A Input ---
    st.markdown("### 💬 Raise your query")
    query = st.chat_input("Ask something...")

    if query:
        result = get_answer_with_sources(gemini_api_key, db, query)
        answer = result.get('answer') or result.get('output_text', "No answer returned.")
        sources = result.get('sources', "No sources available.")

        st.session_state.qa_history.append((query, answer))
        st.session_state.query_count += 1

        with st.chat_message("user"):
            st.markdown(f"**You:** {query}")
        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {answer}")

        if isinstance(sources, list):
            st.markdown("#### 📎 Sources Used")
            for src in sources:
                st.markdown(f"- `{src}`")
        else:
            st.markdown(f"**Sources**: {sources}")

        # --- Prescriptive Suggestions ---
        suggestion, action_label = get_prescriptive_suggestion(query)
        if suggestion:
            st.markdown(f"### {suggestion}")
            if st.button(action_label):
                st.success(f"✅ {action_label} has been initiated.")

    # --- Q&A History Display ---
    if st.session_state.qa_history:
        st.markdown("### 📚 Q&A History")
        for q, a in reversed(st.session_state.qa_history):
            with st.chat_message("user"):
                st.markdown(f"*You:* {q}")
            with st.chat_message("assistant"):
                st.markdown(f"*Answer:* {a}")

        buffer = io.StringIO()
        for q, a in st.session_state.qa_history:
            buffer.write(f"Q: {q}\nA: {a}\n\n")
        st.download_button("📥 Download Q&A Session", buffer.getvalue(), file_name="qa_session.txt")

    # --- Metrics ---
    st.markdown("### 📊 Session Stats")
    st.metric("🧠 Questions Asked", st.session_state.query_count)
    st.metric("📎 Files Uploaded", len(uploaded_files))
else:
    st.info("Please upload at least one document to enable Q&A.")
