
import google.generativeai as genai
from langchain.vectorstores.base import VectorStore
from langdetect import detect

def get_answer_with_sources(api_key, db, query, k=3):
    # Detect language of the question
    input_lang = detect(query)
    lang_instruction = {
        "hi": "उत्तर हिंदी में दें।",
        "mr": "उत्तर मराठीमध्ये द्या.",
        "ja": "回答は日本語でしてください。",
        "en": "",  # default English
    }.get(input_lang, "")

    # prompt_text = (
    #     f"Use the following documents to answer the question accurately and concisely.\n\n"
    #     f"{{summaries}}\n\n"
    #     f"Question: {{question}}\n\n"
    #     f"{lang_instruction}"
    # )

    # prompt = PromptTemplate(
    #     input_variables=["summaries", "question"],
    #     template=prompt_text
    # )

    genai.configure(api_key=api_key)

    # Step 1: Get top-k matching chunks from FAISS
    relevant_docs = db.similarity_search(query, k=k)
    print("🔍 Retrieved sources:", [doc.metadata for doc in relevant_docs])


    # Step 2: Prepare context string from documents
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
You are a helpful assistant. Use the context below to answer the question as accurately as possible. 
If the answer cannot be found in the context, say "I couldn't find that information in the uploaded documents."

Context:
{context}

Question: {query}
Answer:
"""

    # Step 3: Call Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    return {
        "answer": response.text,
        "sources": [f"{doc.metadata.get('source', 'Unknown')} (page {doc.metadata.get('page', '?')})" for doc in relevant_docs]

        #"sources": [doc.metadata.get("source", "Unknown") for doc in relevant_docs]
    }



# def get_answer_with_sources(gemini_api_key, db, query):
#     genai.configure(api_key=gemini_api_key)
#     model = genai.GenerativeModel('gemini-pro')

#     related_docs = db.similarity_search(query, k=4)
#     context = "\n\n".join([doc.page_content for doc in related_docs])

#     full_prompt = f"""Context:
# {context}

# Question:
# {query}

# Answer with references to the source context above."""

#     response = model.generate_content(full_prompt)
#     answer = response.text

#     return {
#         "answer": answer,
#         "sources": "\n".join([doc.metadata['source'] for doc in related_docs])
#     }
#     print("DEBUG: chain result =", result)
#     return result