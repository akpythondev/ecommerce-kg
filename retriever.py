"""
Retrieval layer. Runs a structured graph query (a small JSON spec that the LLM writes)
against the NetworkX graph and returns plain data.

Query spec format:
{
  "return_type": "Product",                      # what we want back
  "constraints": [                               # each one is an anchor node + path to the result
      {"node_type": "Brand", "name": "Nike", "path": ["MADE_BY"]},
      {"node_type": "Vendor", "name": "Metro Wholesale", "path": ["SUPPLIES"]}
  ],
  "name_contains": null                          # optional text filter on result names, e.g. "banana"
}
All constraints must match (AND). The walking direction of each relationship
is worked out automatically from RELATIONSHIPS, so the LLM only names the relations.
"""
from graph_builder import RELATIONSHIPS

NODE_TYPES = {"Product", "Brand", "Category", "Vendor", "Customer", "Order"}
MAX_ROWS = 50


def find_nodes(g, node_type, name):
    """Find nodes by type and name (exact match first, then 'contains')."""
    name = name.lower().strip()
    same_type = [(n, d) for n, d in g.nodes(data=True) if d["node_type"] == node_type]
    exact = [n for n, d in same_type if d["name"].lower() == name]
    if exact:
        return exact
    return [n for n, d in same_type if name in d["name"].lower()]


def take_step(g, nodes, relation):
    """Move from a set of nodes across one relationship type."""
    src_type, dst_type = RELATIONSHIPS[relation]
    reached = set()
    for node in nodes:
        node_type = g.nodes[node]["node_type"]
        if node_type == src_type:
            for _, neighbour, edge in g.out_edges(node, data=True):
                if edge["relation"] == relation:
                    reached.add(neighbour)
        elif node_type == dst_type:
            for neighbour, _, edge in g.in_edges(node, data=True):
                if edge["relation"] == relation:
                    reached.add(neighbour)
    return reached


def follow_path(g, start_nodes, path):
    current = set(start_nodes)
    for relation in path:
        current = take_step(g, current, relation)
    return current


def describe(g, node):
    """Turn a node into a readable dict (adds related info for products/orders)."""
    data = g.nodes[node]
    row = {"type": data["node_type"]}
    row.update({k: v for k, v in data.items() if k != "node_type"})

    if data["node_type"] == "Product":
        for _, nb, e in g.out_edges(node, data=True):
            if e["relation"] == "MADE_BY":
                row["brand"] = g.nodes[nb]["name"]
            elif e["relation"] == "IN_CATEGORY":
                row["category"] = g.nodes[nb]["name"]
        for vendor, _, e in g.in_edges(node, data=True):
            if e["relation"] == "SUPPLIES":
                row["vendor"] = g.nodes[vendor]["name"]

    if data["node_type"] == "Order":
        for customer, _, e in g.in_edges(node, data=True):
            if e["relation"] == "PLACED":
                row["customer"] = g.nodes[customer]["name"]
        row["items"] = [
            {"product": g.nodes[p]["name"], "quantity": e["quantity"]}
            for _, p, e in g.out_edges(node, data=True) if e["relation"] == "CONTAINS"
        ]
    return row


def validate_spec(spec):
    if not isinstance(spec, dict):
        raise ValueError("Query spec must be a JSON object")
    if spec.get("return_type") not in NODE_TYPES:
        raise ValueError(f"Bad return_type: {spec.get('return_type')}")
    for c in spec.get("constraints") or []:
        if c.get("node_type") not in NODE_TYPES:
            raise ValueError(f"Bad node_type in constraint: {c.get('node_type')}")
        for rel in c.get("path") or []:
            if rel not in RELATIONSHIPS:
                raise ValueError(f"Unknown relationship: {rel}")


def run_query(g, spec):
    validate_spec(spec)
    return_type = spec["return_type"]

    result = None  # None means "no constraint applied yet"
    for c in spec.get("constraints") or []:
        starts = find_nodes(g, c["node_type"], c["name"])
        reached = follow_path(g, starts, c.get("path") or [])
        reached = {n for n in reached if g.nodes[n]["node_type"] == return_type}
        result = reached if result is None else result & reached

    if result is None:  # no constraints -> all nodes of that type
        result = {n for n, d in g.nodes(data=True) if d["node_type"] == return_type}

    keyword = (spec.get("name_contains") or "").lower().strip()
    if keyword:
        result = {n for n in result if keyword in g.nodes[n]["name"].lower()}

    rows = [describe(g, n) for n in sorted(result)]
    return {"count": len(rows), "results": rows[:MAX_ROWS]}
