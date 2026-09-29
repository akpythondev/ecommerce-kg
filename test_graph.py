from graph_builder import build_graph, check_banana
from retriever import run_query

g = build_graph()
names = lambda r: sorted(x["name"] for x in r["results"])

assert check_banana(g) == 5

r = run_query(g, {"return_type": "Product", "constraints": [
    {"node_type": "Brand", "name": "Nike", "path": ["MADE_BY"]},
    {"node_type": "Vendor", "name": "Metro Wholesale", "path": ["SUPPLIES"]}]})
assert names(r) == ["Nike Air Runner", "Nike Sports Socks"], names(r)

r = run_query(g, {"return_type": "Product", "constraints": [
    {"node_type": "Customer", "name": "Alice Johnson", "path": ["PLACED", "CONTAINS"]}]})
assert names(r) == ["Banana Chips", "Banana Protein Bar", "Nike Air Runner", "Nike Sports Socks"], names(r)

r = run_query(g, {"return_type": "Customer", "constraints": [
    {"node_type": "Product", "name": "Banana Chips", "path": ["CONTAINS", "PLACED"]}]})
assert names(r) == ["Alice Johnson", "David Lee"], names(r)

r = run_query(g, {"return_type": "Vendor", "constraints": [
    {"node_type": "Brand", "name": "Sony", "path": ["MADE_BY", "SUPPLIES"]}]})
assert names(r) == ["Global Imports", "Metro Wholesale"], names(r)

r = run_query(g, {"return_type": "Brand", "constraints": [
    {"node_type": "Category", "name": "Electronics", "path": ["IN_CATEGORY", "MADE_BY"]}]})
assert names(r) == ["Samsung", "Sony"], names(r)

r = run_query(g, {"return_type": "Product", "constraints": [], "name_contains": "banana"})
assert r["count"] == 5, r["count"]

r = run_query(g, {"return_type": "Product", "constraints": [
    {"node_type": "Vendor", "name": "Sunrise Supplies", "path": ["SUPPLIES"]},
    {"node_type": "Category", "name": "Grocery", "path": ["IN_CATEGORY"]}]})
assert names(r) == ["Banana Chips", "Banana Protein Bar", "Organic Oats"], names(r)

try:
    run_query(g, {"return_type": "Robot", "constraints": []})
    raise AssertionError("should have failed")
except ValueError:
    pass

print("All graph tests pass.")
print("Nodes:", g.number_of_nodes(), "Edges:", g.number_of_edges())
