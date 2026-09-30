import json
import os

from dotenv import load_dotenv
from groq import Groq, BadRequestError

load_dotenv()
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
_client = None


def get_client():
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise SystemExit("GROQ_API_KEY is missing")
        _client = Groq(api_key=key, timeout=60.0, max_retries=3)
    return _client


QUERY_SYSTEM_PROMPT = """You convert a user's question about an e-commerce knowledge graph into a JSON graph query.

GRAPH SCHEMA
Node types: Product, Brand, Category, Vendor, Customer, Order
Relationships:
  MADE_BY      Product  -> Brand
  IN_CATEGORY  Product  -> Category
  SUPPLIES     Vendor   -> Product
  PLACED       Customer -> Order
  CONTAINS     Order    -> Product

OUTPUT FORMAT (JSON only, no explanation):
{"return_type": "<node type wanted>",
 "constraints": [{"node_type": "<type of known entity>", "name": "<its name>", "path": ["REL1", "REL2"]}],
 "name_contains": null or "<word that must be in the result name>"}

RULES
- "path" is the list of relationships to walk from the known entity to the wanted node type.
- Several constraints mean AND (all must match).
- Use name_contains for word searches like "products containing banana".
- If there is no known entity, use an empty constraints list.
- Never invent node types or relationships.

EXAMPLES
Q: Which products from brand Nike are supplied by vendor Metro Wholesale?
{"return_type":"Product","constraints":[{"node_type":"Brand","name":"Nike","path":["MADE_BY"]},{"node_type":"Vendor","name":"Metro Wholesale","path":["SUPPLIES"]}],"name_contains":null}

Q: What did Alice Johnson buy?
{"return_type":"Product","constraints":[{"node_type":"Customer","name":"Alice Johnson","path":["PLACED","CONTAINS"]}],"name_contains":null}

Q: Which customers bought Banana Chips?
{"return_type":"Customer","constraints":[{"node_type":"Product","name":"Banana Chips","path":["CONTAINS","PLACED"]}],"name_contains":null}

Q: Which vendors supply Sony products?
{"return_type":"Vendor","constraints":[{"node_type":"Brand","name":"Sony","path":["MADE_BY","SUPPLIES"]}],"name_contains":null}

Q: Which brands sell products in the Electronics category?
{"return_type":"Brand","constraints":[{"node_type":"Category","name":"Electronics","path":["IN_CATEGORY","MADE_BY"]}],"name_contains":null}

Q: Show all products with the word banana.
{"return_type":"Product","constraints":[],"name_contains":"banana"}
"""

ANSWER_SYSTEM_PROMPT = """You answer questions using ONLY the retrieved graph data given to you.
- Do not use outside knowledge and do not guess.
- If the data is empty or does not answer the question, reply exactly:
  "I could not find this in the knowledge graph."
- Mention names and numbers exactly as they appear in the data.
- Keep the answer short and clear."""


def question_to_query(question):
    try:
        response = get_client().chat.completions.create(
            model=MODEL, temperature=0,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": QUERY_SYSTEM_PROMPT},
                      {"role": "user", "content": question}],
        )
        return json.loads(response.choices[0].message.content)
    except (BadRequestError, json.JSONDecodeError):
        return {"unsupported": True}


def answer_from_data(question, retrieved):
    user_msg = f"Question: {question}\n\nRetrieved graph data:\n{json.dumps(retrieved, indent=2)}"
    response = get_client().chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    )
    return response.choices[0].message.content.strip()
