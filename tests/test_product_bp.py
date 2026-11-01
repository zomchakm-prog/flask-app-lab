import unittest
from app import app
from app.products.db import products_table

class ProductBlueprintTestCase(unittest.TestCase):

  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    self.client = app.test_client()
    products_table.truncate()

  def tearDown(self):
    products_table.truncate()

  def test_products_list_page(self):
    """Перевірка відкриття сторінки зі списком товарів"""
    response = self.client.get('/products/')
    self.assertEqual(response.status_code, 200)

  def test_add_product_page_get(self):
    """Перевірка доступності сторінки додавання товару (GET)"""
    response = self.client.get('/products/add')
    self.assertEqual(response.status_code, 200)

  def test_add_product_post(self):
    """Перевірка додавання нового товару через форму (POST)"""
    response = self.client.post('/products/add', data={
        'name': 'Тестовий смартфон',
        'content': 'Чудовий тестовий опис смартфона з необхідною кількістю символів.',
        'price': '999.99',
        'category': 'electronics',
        'quantity': '10'
    }, follow_redirects=True)
    
    self.assertEqual(response.status_code, 200)
    
    
    items = products_table.all()
    self.assertEqual(len(items), 1)
    self.assertEqual(items[0]['name'], 'Тестовий смартфон')
    self.assertEqual(items[0]['price'], 999.99)

  def test_product_detail_page_valid_id(self):
    """Перевірка детальної сторінки існуючого товару"""
    test_item = {
        'id': 1,
        'name': 'Тестовий ноутбук',
        'content': 'Потужний ноутбук для тестів.',
        'price': 1500.0,
        'category': 'electronics',
        'quantity': 3,
        'image': '',
        'created_at': '2026-10-25 12:00:00'
    }
    products_table.insert(test_item)

    response = self.client.get('/products/1')
    self.assertEqual(response.status_code, 200)
    self.assertIn('Тестовий ноутбук'.encode('utf-8'), response.data)

  def test_product_detail_page_invalid_id(self):
    """Перевірка обробки неіснуючого ID"""
    response = self.client.get('/products/999')
    self.assertIn(response.status_code, [404, 302])


if __name__ == '__main__':
  unittest.main()