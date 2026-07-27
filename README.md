#  Startup Idea Validator — Tips Hindawi Challenge (June–July 2026)

🏆 This repository is my official submission for the **Tips Hindawi Challenge (June–July) 2026**.

## 🌐 Live Demo

The application is deployed and running on **Streamlit Community Cloud**:

👉 [Try Startup Idea Validator Live](https://startupideavalidator-up7zuzk6ztkjz5hkv93nca.streamlit.app/)

---

## 👤 Participant Information

| Field | Value |
|---|---|
| **Full Name** | Abdelrahman Mohamed Fathi |
| **Project Name** | Startup Idea Validator |
| **GitHub Username** | `Abdelrahman-18` |
| **Challenge Batch** | June–July 2026 |
| **Training Program** | Large Language Models (LLMs) Program |
| **Organization** | Edrak for AI |

---

# 📖 Project Overview

**AI Startup Validator** is an automated, **RAG-powered evaluation workspace** designed to analyze startup pitch decks, business plans, and investment proposals.

The system uses **LangChain, vector embeddings, and LLM inference** to ingest PDF documents and extract structured insights, including:

- Business model components
- SWOT analysis
- Investment readiness scores
- Risk factors
- Startup evaluation metrics

It also provides an interactive, document-grounded **AI Copilot** that enables users to ask questions and explore their uploaded documents conversationally.

---

# ✨ Features

## 🤖 Interactive AI Copilot

A centralized chat workspace powered by RAG that:

- Answers questions based only on the uploaded document content
- Provides grounded responses from indexed information
- Enables exploratory startup analysis

---

## 📊 Automated RAG Analytical Frameworks

### 🏢 Business Model Breakdown

Automatically extracts and summarizes:

- Industry
- Target audience
- Main problem
- Proposed solution
- Revenue model
- Business strategy

---

### 🔍 SWOT Analysis Matrix

Generates a structured SWOT evaluation:

| Strengths | Weaknesses |
|---|---|
| Internal advantages | Internal limitations |

| Opportunities | Threats |
|---|---|
| External growth possibilities | External risks |

---

### 📈 Investment Readiness Scoring

Evaluates startup maturity based on:

- Scalability
- Innovation
- Team capability
- Product maturity
- Market potential

Outputs:

- Investment readiness score (0–100)
- Key risk factors
- Improvement recommendations


---

## 🔐 Secure Environment Architecture

Implemented secure deployment practices:

- Streamlit Cloud secrets management
- External LLM API communication
- No exposed API credentials

---

# 🛠️ Technologies Used

## Frontend & Dashboard

- Streamlit

## LLM Orchestration & RAG

- LangChain
  - langchain-core
  - langchain-community
  - langchain-huggingface

## LLM Inference & Embeddings

- Hugging Face Inference API
- Model:
  - `Qwen/Qwen2.5-7B-Instruct`
- Embeddings:
  - `sentence-transformers/all-MiniLM-L6-v2`

## Vector Database

- ChromaDB

## Document Processing

- PyPDF
- ReportLab

## Environment Management

- python-dotenv

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Abdelrahman-18/Startup_Idea_Validator.git

cd Startup_Idea_Validator
```

---

## 2. Create Virtual Environment

### macOS/Linux

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

---

# 🚀 Usage

1. Open the application:

```
http://localhost:8501
```

2. Upload a startup pitch deck or business proposal in PDF format.

3. Click:

```
Build Knowledge Base
```

to process the document and create the vector store.

4. Run automated RAG frameworks:

- Business Model Analysis
- SWOT Analysis
- Investment Readiness Evaluation

5. Use the AI Copilot to:

- Ask questions
- Analyze risks
- Explore startup metrics
- Retrieve document-grounded insights

---

# 📸 Demo

## 🏠 AI Startup Validator Dashboard

The main workspace where users upload startup documents, manage the analysis workflow, and access the application's core features.

<img width="1303" height="646" alt="AI Startup Validator Dashboard" src="https://github.com/user-attachments/assets/1c8c0b16-b55b-494a-9a66-5e0bfd748967" />


---

## 📊 Startup Analysis & Business Insights

The automated RAG analysis dashboard that extracts structured startup insights, including business model evaluation, market understanding, and SWOT analysis.

<img width="1303" height="642" alt="Startup Analysis Dashboard" src="https://github.com/user-attachments/assets/7456bd02-c033-43bf-8719-c66507413a84" />


---

## 📈 Investment Readiness Evaluation

An AI-powered scoring system that evaluates startup potential based on scalability, innovation, product maturity, and investment factors.

<img width="1305" height="640" alt="Investment Readiness Score" src="https://github.com/user-attachments/assets/8021cfc9-c4bf-4c30-83f1-a2f7d3f5c3b4" />


---

## 🤖 AI Startup Copilot Chat

A document-grounded conversational assistant that allows users to ask questions and explore insights directly from the uploaded startup documents using RAG.

<img width="1302" height="653" alt="AI Startup Copilot Chat" src="https://github.com/user-attachments/assets/60e03a4b-29e2-4ba2-a737-164467350433" />

---

# 📈 Results

Successfully achieved:

✅ Built a low-latency RAG pipeline capable of processing multi-page PDF documents.

✅ Created a contextual vector retrieval system for document-grounded responses.

✅ Implemented structured output parsing for:

- SWOT analysis
- Business model extraction
- Investment scoring

✅ Successfully deployed the application on Streamlit Community Cloud.

✅ Secured API credentials using serverless environment secrets.

---

# 🔮 Future Improvements

## 📚 Multi-Document Comparison

Enable:

- Comparing multiple startup pitch decks
- Benchmarking competitors
- Ranking investment opportunities

---

## 📄 Exportable Reports

Add:

- Automated PDF reports
- Downloadable startup evaluation summaries
- Investor-ready documents

---

## ☁️ Persistent Cloud Vector Database

Integrate:

- Qdrant
- Pinecone

for:

- Persistent storage
- Multi-session usage
- Scalable document retrieval

---


# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---


# 📄 License

This project is shared for educational and portfolio purposes.
