
import csv
from pathlib import Path

import networkx as nx

DATA_DIR = Path(__file__).parent / "data"

RELATIONSHIPS = {
    "MADE_BY": ("Product", "Brand"),        
    "IN_CATEGORY": ("Product", "Category"), 
    "SUPPLIES": ("Vendor", "Product"),      
    "PLACED": ("Customer", "Order"),         
    "CONTAINS": ("Order", "Product"),       
}

BANANA_WORD = "banana"
BANANA_EXPECTED = 5


def read_csv(filename):
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_node(g, node_type, key, name, **props):
    """Node id looks like 'Brand:Nike' so ids never clash between types."""
    node_id = f"{node_type}:{key}"
    if node_id not in g:
        g.add_node(node_id, node_type=node_type, name=name, **props)
    return node_id


def build_graph():
    g = nx.DiGraph()

    for row in read_csv("products.csv"):
        product = add_node(g, "Product", row["product_id"], row["name"],
                           price=float(row["price"]))
        brand = add_node(g, "Brand", row["brand"], row["brand"])
        category = add_node(g, "Category", row["category"], row["category"])
        vendor = add_node(g, "Vendor", row["vendor"], row["vendor"])

        g.add_edge(product, brand, relation="MADE_BY")
        g.add_edge(product, category, relation="IN_CATEGORY")
        g.add_edge(vendor, product, relation="SUPPLIES")

    for row in read_csv("customers.csv"):
        add_node(g, "Customer", row["customer_id"], row["name"], city=row["city"])

    for row in read_csv("orders.csv"):
        order = add_node(g, "Order", row["order_id"], row["order_id"],
                         order_date=row["order_date"])
        g.add_edge(f"Customer:{row['customer_id']}", order, relation="PLACED")

    for row in read_csv("order_items.csv"):
        g.add_edge(f"Order:{row['order_id']}", f"Product:{row['product_id']}",
                   relation="CONTAINS", quantity=int(row["quantity"]))

    return g


def count_banana(g):
    """Counts how many times the word 'banana' appears in node values."""
    total = 0
    for _, data in g.nodes(data=True):
        for value in data.values():
            if isinstance(value, str):
                total += value.lower().count(BANANA_WORD)
    return total


def check_banana(g):
    found = count_banana(g)
    if found != BANANA_EXPECTED:
        raise ValueError(f"'banana' should appear {BANANA_EXPECTED} times, found {found}")
    return found


if __name__ == "__main__":
    graph = build_graph()
    print("Nodes:", graph.number_of_nodes(), "| Edges:", graph.number_of_edges())
    print("Banana count:", check_banana(graph))
