# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Abdelrahman Mohamed Fathi            |
| Project Name     | AI Startup Validator                 |
| GitHub Username  | `[Your-GitHub-Username]`             |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

**AI Startup Validator** is an automated, RAG-powered evaluation workspace built to analyze startup pitch decks, business plans, and investment proposals. Utilizing LangChain, vector embeddings, and LLM inference, the system ingests PDF documents to extract structured insights—including business model components, SWOT analyses, and investment readiness scores—while providing an interactive, document-grounded AI Copilot for conversational analysis.

---

# ✨ Features

* **Interactive AI Copilot**: Centrally positioned chat workspace grounded strictly in the indexed document content for custom QA and exploratory analysis.
* **Automated RAG Analytical Frameworks**:
  * **Business Model Breakdown**: Summarizes industry, target audience, key problem, proposed solution, and revenue models.
  * **SWOT Analysis Matrix**: Automatically categorizes Strengths, Weaknesses, Opportunities, and Threats into a clean UI matrix.
  * **Investment Readiness Scoring**: Evaluates scalability, innovation, team, and product maturity to output a score (0–100) with risk factors.
* **Secure Environment Architecture**: Integrated with Streamlit Cloud secrets management to process requests via external LLM endpoints without exposing API credentials.

---

# 🛠️ Technologies Used

* **Frontend & Dashboard**: Streamlit
* **LLM Orchestration & RAG**: LangChain (`langchain-core`, `langchain-community`, `langchain-huggingface`)
* **Inference API & Models**: Hugging Face Inference API (`Qwen/Qwen2.5-7B-Instruct`), Hugging Face Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Database**: ChromaDB
* **Document Handling & Generation**: PyPDF, ReportLab
* **Environment & Config**: `python-dotenv`

---

# ⚙️ Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/Startup_Idea_Validator.git](https://github.com/YOUR_GITHUB_USERNAME/Startup_Idea_Validator.git)
   cd Startup_Idea_Validator
