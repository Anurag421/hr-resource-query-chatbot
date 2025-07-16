from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag_engine import load_employees, search_employees

app = FastAPI(title="HR Resource Chatbot API")

# Load employee data once at startup
employees = load_employees()

# Enable CORS for frontend usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema for /chat endpoint
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "✅ HR Resource Chatbot is running!"}

@app.get("/employees/search")
def search_employees_get(query: str):
    matched, _ = search_employees(query, employees)
    return {"results": matched}

@app.post("/chat")
def chat_with_bot(request: QueryRequest):
    query = request.query
    matched_employees, gpt_response = search_employees(query, employees)
    return {
        "response": gpt_response,
        "results": matched_employees
    }
