# Sample questions and results

## 1. Which products from brand Nike are supplied by vendor Metro Wholesale?
**Graph query:** `{'return_type': 'Product', 'constraints': [{'node_type': 'Brand', 'name': 'Nike', 'path': ['MADE_BY']}, {'node_type': 'Vendor', 'name': 'Metro Wholesale', 'path': ['SUPPLIES']}], 'name_contains': None}`

**Retrieved rows:** 2

**Answer:** Nike Air Runner  
Nike Sports Socks

## 2. What did Alice Johnson buy?
**Graph query:** `{'return_type': 'Product', 'constraints': [{'node_type': 'Customer', 'name': 'Alice Johnson', 'path': ['PLACED', 'CONTAINS']}], 'name_contains': None}`

**Retrieved rows:** 4

**Answer:** I could not find this in the knowledge graph.

## 3. Which customers bought Banana Chips?
**Graph query:** `{'return_type': 'Customer', 'constraints': [{'node_type': 'Product', 'name': 'Banana Chips', 'path': ['CONTAINS', 'PLACED']}], 'name_contains': None}`

**Retrieved rows:** 2

**Answer:** Alice Johnson and David Lee.

## 4. Which vendors supply Sony products?
**Graph query:** `{'return_type': 'Vendor', 'constraints': [{'node_type': 'Brand', 'name': 'Sony', 'path': ['MADE_BY', 'SUPPLIES']}], 'name_contains': None}`

**Retrieved rows:** 2

**Answer:** The vendors that supply Sony products are:

- Global Imports  
- Metro Wholesale

## 5. Which brands sell products in the Electronics category?
**Graph query:** `{'return_type': 'Brand', 'constraints': [{'node_type': 'Category', 'name': 'Electronics', 'path': ['IN_CATEGORY', 'MADE_BY']}], 'name_contains': None}`

**Retrieved rows:** 2

**Answer:** Samsung, Sony

## 6. Show all products that contain the word banana.
**Graph query:** `{'return_type': 'Product', 'constraints': [], 'name_contains': 'banana'}`

**Retrieved rows:** 5

**Answer:** - Banana Chips  
- Banana Protein Bar  
- Banana Face Mask  
- Banana Hair Shampoo  
- Banana Scented Candle

## 7. Which products are supplied by Sunrise Supplies and belong to the Grocery category?
**Graph query:** `{'return_type': 'Product', 'constraints': [{'node_type': 'Vendor', 'name': 'Sunrise Supplies', 'path': ['SUPPLIES']}, {'node_type': 'Category', 'name': 'Grocery', 'path': ['IN_CATEGORY']}], 'name_contains': None}`

**Retrieved rows:** 3

**Answer:** Banana Chips, Banana Protein Bar, Organic Oats
