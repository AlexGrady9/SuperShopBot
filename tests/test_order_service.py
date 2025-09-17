import unittest
import json
from services import order_service
from data.orders import ORDERS_PATH


class TestOrderService(unittest.TestCase):
    def setUp(self):
        # Backup and clear orders file
        try:
            with open(ORDERS_PATH, 'r', encoding='utf-8') as f:
                self._backup = f.read()
        except FileNotFoundError:
            self._backup = ''
        with open(ORDERS_PATH, 'w', encoding='utf-8') as f:
            f.write('')

    def tearDown(self):
        # Restore orders file
        with open(ORDERS_PATH, 'w', encoding='utf-8') as f:
            f.write(self._backup)

    def test_save_and_get_orders(self):
        order = {"name": "Test User", "phone": "+1234567890",
                 "address": "Test Street", "items": [1, 2]}
        order_service.save_order(order)
        orders = order_service.get_orders()
        self.assertIsInstance(orders, list)
        self.assertGreater(len(orders), 0)
        self.assertEqual(orders[0]['name'], "Test User")


if __name__ == '__main__':
    unittest.main()
