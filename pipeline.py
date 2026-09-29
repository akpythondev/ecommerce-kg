from graph_builder import build_graph, check_banana
from llm import answer_from_data, question_to_query
from retriever import run_query

graph = build_graph()
check_banana(graph)  

NOT_FOUND = "I could not find this in the knowledge graph."

def ask(question):
    try:
        query = question_to_query(question)

        if query.get("unsupported") or not query.get("return_type"):
            return {"question": question, "query": query,
                    "retrieved": {"count": 0, "results": []}, "answer": NOT_FOUND}

        retrieved = run_query(graph, query)
        answer = answer_from_data(question, retrieved)
    except ValueError as err:
        return {"question": question, "query": None, "retrieved": None,
                "answer": f"Could not build a valid graph query: {err}"}
    except Exception as err:
        return {"question": question, "query": None, "retrieved": None,
                "answer": f"LLM connection problem, please try again. ({type(err).__name__})"}
    return {"question": question, "query": query, "retrieved": retrieved, "answer": answer}