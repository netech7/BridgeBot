# BridgeBot: Smart Information Retrieval Assistant

**BridgeBot** is an AI-powered assistant designed to automate document retrieval and analytics within enterprise departments such as IT, GRC, and HR. Built during an internship at Bridgestone India, the assistant supports natural language queries and descriptive analysis over structured and unstructured internal documents.

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
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run main.py
```

---

## 🔐 API Key Setup Instructions

Before running the app, you must generate your encrypted Gemini API key.

### 🔧 Step-by-Step

1. Run the following script to generate the necessary encryption files:

   ```bash
   python key_setup.py
   
The script will:
Prompt you to enter your Gemini API key
Generate two files:
```
fernet.key
encrypted_key.bin
```

These files are required at runtime and must be kept in the root project directory.
> Note: These files are intentionally excluded from Git version control via .gitignore for security reasons.

---

## 🔐 Security & .gitignore Notes

### 🔒 API Key Protection

- API keys are encrypted using **Fernet**.
- This project uses **AES-128-CBC encryption** with **HMAC-SHA256** integrity checks via `cryptography.fernet`.

### 📂 .gitignore

The `.gitignore` file prevents sensitive and unnecessary files from being committed:

```gitignore
# Secrets & Config
.env
key_config.py

# Python Env & Cache
venv/
__pycache__/
*.pyc

# System & IDE
.DS_Store
.vscode/
.idea/
```

---

## 📊 Analytics Capabilities

- **Descriptive Analytics (implemented):**  
  Auto-charting of Excel data, summary statistics, and keyword extraction.

- **Predictive Analytics (planned):**  
  Forecast trends from audit logs or document usage.

- **Prescriptive Analytics (planned):**  
  Recommend actions based on document patterns or triggers.

---

## ⚠️ Limitations

- This version uses the **free Gemini API**, which is not suitable for production due to:
  - Rate limits
  - No enterprise-grade data retention guarantees

- Due to internship-level access, this was **not deployed on Bridgestone’s Microsoft Azure infrastructure** or internal SharePoint systems.

- Enterprise deployment should use **Azure OpenAI** or **on-prem LLMs** for secure integration.

---

## 📬 Handover & Contact

**Project Name:** BridgeBot – Empowering digital transformation  
**Developer:** Nehal Jain  
**Internship Duration:** May 2025 – June 2025  
**Company:** Bridgestone India  
**Contact:** emailnehaljain@gmail.com

> For setup or further support, please refer to the instructions above or contact the author directly.

---

## 📄 License & Usage

This project is intended for internal use and demonstration only.  
Do not deploy in production environments without code review, security audit, and legal approval.
