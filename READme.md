# BridgeAI: Smart Document Assistant

**BridgeAI** is an AI-powered assistant designed to automate document retrieval and analytics within enterprise departments such as IT, GRC, and HR. Built during an internship at Bridgestone India, the assistant supports natural language queries and descriptive analysis over structured and unstructured internal documents.

---

## 🔍 Features

- Secure upload and parsing of PDF, Word, Excel, and scanned documents
- Natural language query interface with document-aligned answers
- Embedding-based search using FAISS
- Automated charting for Excel data
- Frontend in Streamlit, backend in FastAPI
- Secure API key encryption using Fernet (AES-CBC)
- Descriptive analytics engine for contextual summaries

---

## 🧰 Tech Stack

| Layer           | Tools Used                                 |
|----------------|---------------------------------------------|
| Frontend        | Streamlit                                   |
| Backend         | FastAPI, LangChain, Gemini API              |
| NLP / Embedding | Gemini Embedding API, LangChain             |
| Vector Store    | FAISS (in-memory vector similarity search)  |
| Document Parsing| PyMuPDF, pytesseract, python-docx, pandas   |
| Visualization   | Matplotlib, Seaborn                         |
| Security        | cryptography (Fernet AES-CBC encryption)    |

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/bridgeai-doc-assistant.git
cd bridgeai-doc-assistant

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies
```bash
pip install -r requirements.txt

### 5. Run the Application
```bash
streamlit run main.py
