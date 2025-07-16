import json
import openai
import os
from dotenv import load_dotenv
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load OpenAI API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to employee JSON
DATA_PATH = "backend/data/employees.json"

# Load employee profiles
def load_employees() -> List[dict]:
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or "employees" not in data:
            raise ValueError("Invalid format: JSON must contain 'employees' key.")
        employees = data["employees"]
        if not isinstance(employees, list) or not all(isinstance(emp, dict) for emp in employees):
            raise ValueError("Invalid format: 'employees' must be a list of dictionaries.")
        return employees
    except Exception as e:
        print(f"⚠️ Error loading employees: {e}")
        return []

# Build a TF-IDF vector index from employee data
def build_vector_index(employees: List[dict]) -> Tuple:
    try:
        docs = [
            f"{emp['name']} {' '.join(emp['skills'])} {' '.join(emp['projects'])} {emp['experience_years']} years experience"
            for emp in employees
        ]
        vectorizer = TfidfVectorizer().fit_transform(docs)
        return vectorizer, docs
    except Exception as e:
        print(f"⚠️ Error building vector index: {e}")
        return None, []

# Search function using cosine similarity and GPT response generation
def search_employees(query: str, employees: List[dict]) -> Tuple[List[dict], str]:
    index, docs = build_vector_index(employees)
    if index is None or not docs:
        return [], "⚠️ Unable to process search due to internal error."

    try:
        query_vec = TfidfVectorizer().fit(docs).transform([query])
        scores = cosine_similarity(query_vec, index).flatten()

        # Get top 2 matches
        top_indices = scores.argsort()[::-1][:2]
        matched = [employees[i] for i in top_indices]

        # Format profiles for GPT prompt
        formatted_profiles = "\n\n".join(
            f"Name: {emp['name']}\n"
            f"Experience: {emp['experience_years']} years\n"
            f"Skills: {', '.join(emp['skills'])}\n"
            f"Projects: {', '.join(emp['projects'])}\n"
            f"Availability: {emp['availability']}"
            for emp in matched
        )

        prompt = (
            f"You are an HR assistant. A manager asked:\n"
            f"'{query}'\n\n"
            f"Based on the employee profiles below, suggest top matches in a helpful tone.\n\n"
            f"{formatted_profiles}\n\n"
            f"Your response:"
        )

        try:
            gpt_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            reply = gpt_response["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"⚠️ GPT error: {str(e)}"

        return matched, reply

    except Exception as e:
        return [], f"⚠️ Search failure: {str(e)}"
