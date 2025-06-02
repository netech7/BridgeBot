import streamlit as st
import os
from utils.ingest import load_and_split_pdf, create_vector_store
from utils.qa import get_answer
from utils.translate import translate_to_english, translate_from_english

st.set_page_config(page_title="Bot", layout="centered")
st.title("📄 Automated IT policy extraction")

# Upload document
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file:
    file_path = f"documents/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("⏳ Processing document...")
    chunks = load_and_split_pdf(file_path)
    create_vector_store(chunks)
    st.success("✅ Document indexed successfully!")

# Ask question
query = st.text_input("Raise your query:")

if query:
    translated_query, lang = translate_to_english(query)
    answer_en = get_answer(translated_query)
    final_answer = translate_from_english(answer_en, lang)
    
    st.markdown("**Answer:**")
    st.success(final_answer)
