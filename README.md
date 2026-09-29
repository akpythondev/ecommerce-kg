# E-commerce Knowledge Graph with AI Retrieval

This project builds a small knowledge graph for e-commerce data using Python and NetworkX.
You can ask questions in normal English and the system gives the answer from the graph data only.

Flow:

```
User Question -> LLM -> Graph Query -> Get Data from Graph -> LLM -> Answer
```

## Tech Used
- Python 3.10 or above
- NetworkX (for the graph)
- Groq API with `openai/gpt-oss-120b` model (free key)
- FastAPI (optional, for API)

## Setup

1. Open the project folder `ecommerce_kg` in the terminal
```bash
cd ecommerce_kg
```

2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
```

3. Install the packages
```bash
pip install -r requirements.txt
```

4. Add your API key
   - Get a free key from https://console.groq.com/keys
   - Paste it in `.env`:
```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

## How to Run

| Task | Command |
|------|---------|
| Test graph (no API key needed) | `python test_graph.py` |
| Check graph and banana count | `python graph_builder.py` |
| Chat mode | `python main.py` |
| Ask one question | `python main.py "What did Alice Johnson buy?"` |
| Run all sample questions | `python run_samples.py` |
| Start API | `uvicorn api:app --reload` |

`run_samples.py` saves all the results in `sample_results.md`.

## Dataset
The data is in the `data` folder as CSV files:
- `products.csv`
- `customers.csv`
- `orders.csv`
- `order_items.csv`

It has 17 products, 5 brands, 5 categories, 4 vendors, 6 customers and 10 orders.

## Knowledge Graph

Node types: Product, Brand, Category, Vendor, Customer, Order
(48 nodes and 80 edges in total)

| Relationship | Meaning |
|---|---|
| MADE_BY | Product -> Brand |
| IN_CATEGORY | Product -> Category |
| SUPPLIES | Vendor -> Product |
| PLACED | Customer -> Order |
| CONTAINS | Order -> Product (with quantity) |

## How It Works

1. The user asks a question.
2. The LLM reads the question and creates a small JSON graph query. Example:
```json
{
  "return_type": "Product",
  "constraints": [
    {"node_type": "Brand", "name": "Nike", "path": ["MADE_BY"]},
    {"node_type": "Vendor", "name": "Metro Wholesale", "path": ["SUPPLIES"]}
  ]
}
```
3. `retriever.py` checks the query, finds the nodes in the graph, follows the relationships and returns the matching data.
4. The data is sent to the LLM again and it writes the final answer.

I used a JSON query instead of Cypher because NetworkX has no query language. This also stops the LLM from running wrong queries, because the code validates every query first.

## Answers Only From Graph Data
- The answer prompt tells the LLM to use only the retrieved data.
- Temperature is 0, so the answers stay stable.
- If nothing is found, the answer is "I could not find this in the knowledge graph."
- The query and the row count are printed with every answer, so it can be checked.

## Banana Requirement
The word "banana" is added exactly 5 times, in the names of 5 products:
- Banana Chips
- Banana Protein Bar
- Banana Face Mask
- Banana Hair Shampoo
- Banana Scented Candle

The function `count_banana()` in `graph_builder.py` counts the word in all node values. If the count is not 5, the app will not start.

To get them, ask: "Show all products that contain the word banana."

## Sample Questions
1. Which products from brand Nike are supplied by vendor Metro Wholesale?
2. What did Alice Johnson buy?
3. Which customers bought Banana Chips?
4. Which vendors supply Sony products?
5. Which brands sell products in the Electronics category?
6. Show all products that contain the word banana.
7. Which products are supplied by Sunrise Supplies and belong to the Grocery category?

Full answers are in `sample_results.md`.

## Project Files
- `graph_builder.py` - builds the graph and checks banana count
- `retriever.py` - runs the graph queries
- `llm.py` - Groq LLM prompts and calls
- `pipeline.py` - connects the full flow
- `main.py` - chat in terminal
- `run_samples.py` - runs sample questions
- `api.py` - optional FastAPI
- `test_graph.py` - tests without LLM