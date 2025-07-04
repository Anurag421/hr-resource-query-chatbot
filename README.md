![image](https://github.com/user-attachments/assets/61cf6144-5040-4461-8671-4ced929c8c1d)

# HR Resource Query Chatbot
## Overview

The HR Resource Query Chatbot is an AI-powered assistant built to help HR teams find suitable employees by answering natural language queries like:

- "Find Python developers with 3+ years experience"
- "Who has worked on healthcare projects?"
- "Suggest people for a React Native project"

The system uses semantic search and AI augmentation to match HR needs with employee profiles efficiently.

---

## Features

- 🔍 Search employees using natural language
- 🤖 Embedding-based semantic retrieval
- 📄 FastAPI backend with REST endpoints
- 💬 Streamlit frontend for easy chat experience
- 🧠 OpenAI API integration for smart recommendations (blocked temporarily due to quota)
- 🔎 Auto-generated OpenAPI docs with FastAPI

---

## Architecture

[Streamlit Frontend] <--> [FastAPI Backend] <--> [RAG Engine (Embeddings)] <--> [Employee JSON Dataset]


- **Frontend**: Streamlit UI to input queries and display matched results  
- **Backend**: FastAPI serving REST endpoints `/chat` and `/employees/search`  
- **RAG Engine**: Embedding-based search and response augmentation  
- **Data**: Sample dataset with 15+ employees and their details  

---

## Setup & Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/hr-resource-query-chatbot.git
cd hr-resource-query-chatbot
```
### Step 2: Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run FastAPI backend

```bash
uvicorn backend.main:app --reload
```

### Step 4: Run Streamlit frontend

```bash
streamlit run streamlit_app.py
```
---

# API Documentation
### POST /chat
Query the chatbot with natural language:

```json
{
  "query": "Find Python developers with 3+ years experience"
}
```
### Response:

```json

{
  "results": [
    {
      "name": "Alice Johnson",
      "skills": ["Python", "React", "AWS"],
      "projects": ["E-commerce Platform", "Healthcare Dashboard"],
      "availability": "available"
    },
    ...
  ]
}

```
### GET /employees/search

Search employees with query parameters:

```bash
/employees/search?query=aws developer
```

---

# AI Development Process

Tools Used: ChatGPT, Cursor AI

### AI Helped With:

Initial architecture suggestions

Code generation (FastAPI, Streamlit)

Bug fixing and error debugging

JSON data formatting

#### AI Usage Estimate: ~60% AI-assisted, 40% manually refined

# Manual Challenges:

Debugging OpenAI SDK versioning issues

Handling quota exceeded errors

Streamlit API layout alignment

#### Technical Decisions
Model: OpenAI Embeddings API used (fallbacks under consideration)

Backend: FastAPI for async and API documentation ease

Frontend: Streamlit for quick prototyping

### Reasoning:

OpenAI chosen for simplicity and reliability

No FAISS due to time constraints and small dataset

### Future Improvements

🔁 Add FAISS vector index for faster, scalable search

💬 Integrate response generation from OpenAI once quota recharged

🌍 Deploy to Streamlit Cloud or HuggingFace Spaces

🔒 Add authentication for secure access

📈 Expand dataset to >100 realistic employee profiles

---

## Demo
Local API Docs: [http://localhost:8000/docs](http://127.0.0.1:8000/docs)
Streamlit UI: [http://localhost:8501](http://localhost:8502/)
