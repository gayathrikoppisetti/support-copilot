from fastapi import FastAPI
from pydantic import BaseModel
from generate import answer_question
from verify import verify_answer

app = FastAPI(title="Taskly Support Copilot")


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: QuestionRequest):
    result = verify_answer(request.question)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}
