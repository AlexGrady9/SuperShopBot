import unittest
from services import product_service


class TestProductService(unittest.TestCase):
    def test_load_products(self):
        products = product_service.load_products()
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)
        self.assertIn('name', products[0])

    def test_get_categories(self):
        categories = product_service.get_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)

    def test_get_products_by_category(self):
        categories = product_service.get_categories()
        for category in categories:
            products = product_service.get_products_by_category(category)
            self.assertIsInstance(products, list)
            for product in products:
                self.assertEqual(product['category'], category)


if __name__ == '__main__':
    unittest.main()
