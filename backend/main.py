from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import load_employees, search_employees

app = FastAPI()

# Load employee data once
employees = load_employees()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QueryRequest(BaseModel):
    query: str

# Root route
@app.get("/")
def home():
    return {"message": "HR Resource Chatbot is running!"}

# Search endpoint (for frontend)
@app.get("/employees/search")
def search_employees_get(query: str):
    matched, _ = search_employees(query, employees)
    return {"results": matched}

# Chat endpoint (for chatbot use)
@app.post("/chat")
def chat_with_bot(request: QueryRequest):
    query = request.query
    matched, descriptions = search_employees(query, employees)

    response = {
        "message": f"Based on your query: '{query}', here are some matches:",
        "results": []
    }

    for emp, desc in zip(matched, descriptions):
        response["results"].append({
            "name": emp["name"],
            "skills": emp["skills"],
            "experience_years": emp["experience_years"],
            "projects": emp["projects"],
            "availability": emp["availability"],
            "match_description": desc
        })

    return response
