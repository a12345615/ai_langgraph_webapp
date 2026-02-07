from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import traceback

try:
    from grapy import graph_app
    print("✓ Successfully loaded grapy")
except Exception as e:
    
    print(f"ERROR loading grapy: {e}")
    traceback.print_exc()
    graph_app = None


app = FastAPI(title="LangGraph + Groq WebApp")

# Serve static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    print("✓ Successfully mounted static files")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    intent: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"<h1>Error loading index.html: {e}</h1>"

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if graph_app is None:
        raise HTTPException(status_code=500, detail="Graph application failed to load")
    
    try:
        print(f"Processing question: {req.question}")
        state = {"user_input": req.question, "intent": "general", "answer": ""}
        print("Invoking graph...")
        out = graph_app.invoke(state)
        print(f"Graph returned: {out}")
        return {"answer": out.get("answer", ""), "intent": out.get("intent", "general")}
    except Exception as e:
        print(f"ERROR in /ask: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

print("✓ App module loaded successfully")
