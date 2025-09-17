import json
from data.products import PRODUCTS_PATH


def load_products():
    with open(PRODUCTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_categories():
    products = load_products()
    return list({p['category'] for p in products})


def get_products_by_category(category):
    products = load_products()
    return [p for p in products if p['category'] == category]
