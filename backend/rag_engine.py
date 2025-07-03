import os
import json
import faiss
import openai
import numpy as np
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
EMPLOYEE_DATA_PATH = "backend/data/employees.json"
VECTOR_STORE_PATH = "backend/vector_stores/index.faiss"

# ----------- Helper Functions -----------

def load_employees():
    with open(EMPLOYEE_DATA_PATH, "r") as f:
        data = json.load(f)
    return data["employees"]

def format_employee(employee):
    return f"{employee['name']} is a {employee['experience_years']} years experienced developer skilled in {', '.join(employee['skills'])}. Past projects: {', '.join(employee['projects'])}. Availability: {employee['availability']}."

def embed_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response['data'][0]['embedding'], dtype=np.float32)

# ----------- Indexing -----------

def build_vector_index(employees):
    documents = [format_employee(emp) for emp in employees]
    embeddings = [embed_text(doc) for doc in documents]

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, VECTOR_STORE_PATH)
    return index, documents

def load_vector_index(employees):
    if os.path.exists(VECTOR_STORE_PATH):
        index = faiss.read_index(VECTOR_STORE_PATH)
        documents = [format_employee(emp) for emp in employees]
    else:
        index, documents = build_vector_index(employees)
    return index, documents

# ----------- Search Interface -----------

def search_employees(query, employees, top_k=3):
    query_embedding = embed_text(query)
    index, documents = load_vector_index(employees)

    distances, indices = index.search(np.array([query_embedding]), top_k)
    results = [documents[i] for i in indices[0]]

    matched_employees = [employees[i] for i in indices[0]]
    return matched_employees, results
