from fastapi import FastAPI
from pydantic import BaseModel

from graph_builder import count_banana
from pipeline import ask, graph

app = FastAPI(title="E-commerce Knowledge Graph")


class Question(BaseModel):
    question: str


@app.get("/stats")
def stats():
    return {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(),
            "banana_count": count_banana(graph)}


@app.post("/ask")
def ask_question(body: Question):
    return ask(body.question)
