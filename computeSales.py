#!/usr/bin/env python3
"""
computeSales.py

Computes total sales cost based on a product price catalogue
and a sales record, both provided in JSON format.
"""
# pylint: disable=invalid-name
import json
import sys
import time


def load_json_file(file_path):
    """Load a JSON file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: File not found -> {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON format -> {file_path}")
        return None


def build_price_catalogue(products):
    """Build a dictionary with product titles as keys and prices as values."""
    catalogue = {}

    for product in products:
        try:
            title = product["title"]
            price = float(product["price"])
            catalogue[title] = price
        except (KeyError, ValueError, TypeError):
            print(f"ERROR: Invalid product entry skipped -> {product}")

    return catalogue


def compute_sales_total(sales, catalogue):
    """Compute total sales cost."""
    sale_totals = {}
    grand_total = 0.0

    for record in sales:
        try:
            sale_id = record["SALE_ID"]
            product_name = record["Product"]
            quantity = int(record["Quantity"])

            if product_name not in catalogue:
                print(f"ERROR: Product not found -> {product_name}")
                continue

            cost = catalogue[product_name] * quantity

            if sale_id not in sale_totals:
                sale_totals[sale_id] = 0.0

            sale_totals[sale_id] += cost
            grand_total += cost

        except (KeyError, ValueError, TypeError):
            print(f"ERROR: Invalid sales record skipped -> {record}")

    return sale_totals, grand_total


def write_results(sale_totals, grand_total, elapsed_time):
    """Write results to file and print to console."""
    with open("SalesResults.txt", "w", encoding="utf-8") as file:
        header = "SALES SUMMARY\n" + "-" * 30 + "\n"
        print(header)
        file.write(header)

        for sale_id in sorted(sale_totals):
            line = f"Sale ID {sale_id}: ${sale_totals[sale_id]:.2f}\n"
            print(line.strip())
            file.write(line)

        footer = (
            "-" * 30 + "\n"
            f"TOTAL SALES: ${grand_total:.2f}\n"
            f"Execution Time: {elapsed_time:.6f} seconds\n"
        )

        print(footer)
        file.write(footer)


def main():
    if len(sys.argv) != 3:
        print(
            "Usage:\n"
            "python computeSales.py TC1.ProductList.json TC1.Sales.json"
        )
        sys.exit(1)

    start_time = time.time()

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    products = load_json_file(product_file)
    sales = load_json_file(sales_file)

    if products is None or sales is None:
        sys.exit(1)

    catalogue = build_price_catalogue(products)
    sale_totals, grand_total = compute_sales_total(sales, catalogue)

    elapsed_time = time.time() - start_time
    write_results(sale_totals, grand_total, elapsed_time)


if __name__ == "__main__":
    main()
