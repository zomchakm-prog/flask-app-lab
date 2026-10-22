import unittest
from app import app


class ProductBlueprintTestCase(unittest.TestCase):

  def setUp(self):
    app.config['TESTING'] = True
    self.client = app.test_client()

  def test_products_list_page(self):
    response = self.client.get('/products/')
    self.assertEqual(response.status_code, 200)
    self.assertIn('Laptop'.encode('utf-8'), response.data)

  def test_product_detail_page_valid_id(self):
    response = self.client.get('/products/1')
    self.assertEqual(response.status_code, 200)
    self.assertIn('Laptop'.encode('utf-8'), response.data)

  def test_product_detail_page_invalid_id(self):
    response = self.client.get('/products/999')
    self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
  unittest.main()