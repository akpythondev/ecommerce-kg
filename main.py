import json
import sys

from pipeline import ask, graph
from graph_builder import count_banana


def show(result):
    print("\nGraph query :", json.dumps(result["query"]))
    if result["retrieved"] is not None:
        print("Rows found  :", result["retrieved"]["count"])
    print("Answer      :", result["answer"], "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show(ask(" ".join(sys.argv[1:])))
    else:
        print(f"Graph loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges, "
              f"'banana' count = {count_banana(graph)}")
        print("Ask a question (type 'exit' to quit)")
        while True:
            q = input("\n> ").strip()
            if q.lower() in ("exit", "quit", ""):
                break
            show(ask(q))
