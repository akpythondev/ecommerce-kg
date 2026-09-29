from pipeline import ask

QUESTIONS = [
    "Which products from brand Nike are supplied by vendor Metro Wholesale?",
    "What did Alice Johnson buy?",
    "Which customers bought Banana Chips?",
    "Which vendors supply Sony products?",
    "Which brands sell products in the Electronics category?",
    "Show all products that contain the word banana.",
    "Which products are supplied by Sunrise Supplies and belong to the Grocery category?",
]

if __name__ == "__main__":
    lines = ["# Sample questions and results\n"]
    for i, q in enumerate(QUESTIONS, 1):
        r = ask(q)
        print(f"{i}. {q}\n   -> {r['answer']}\n")
        lines += [f"## {i}. {q}", f"**Graph query:** `{r['query']}`", "",
                  f"**Retrieved rows:** {r['retrieved']['count'] if r['retrieved'] else 0}", "",
                  f"**Answer:** {r['answer']}", ""]
    with open("sample_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Saved to sample_results.md")
