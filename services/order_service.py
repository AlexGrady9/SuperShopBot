import json
from data.orders import ORDERS_PATH


def save_order(order):
    """Save a new order to the orders JSON file."""
    with open(ORDERS_PATH, 'a', encoding='utf-8') as f:
        json.dump(order, f, ensure_ascii=False)
        f.write('\n')


def get_orders():
    """Load all orders from the orders JSON file."""
    with open(ORDERS_PATH, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]
