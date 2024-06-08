# test_app.py

import unittest
from app import app, inventory

class InventoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        inventory.clear()

    def test_add_item(self):
        response = self.app.post('/add_item', json={
            'billOfLading': 'BOL123',
            'itemName': 'Test Item',
            'itemQuantity': 10,
            'itemPrice': 25.5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('BOL123', data)
        self.assertEqual(data['BOL123']['name'], 'Test Item')
        self.assertEqual(data['BOL123']['quantity'], 10)
        self.assertEqual(data['BOL123']['price'], 25.5)

    def test_get_inventory(self):
        inventory['BOL123'] = {
            'name': 'Test Item',
            'quantity': 10,
            'price': 25.5
        }
        response = self.app.get('/get_inventory')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('BOL123', data)
        self.assertEqual(data['BOL123']['name'], 'Test Item')
        self.assertEqual(data['BOL123']['quantity'], 10)
        self.assertEqual(data['BOL123']['price'], 25.5)

    def test_upload_file(self):
        with open('test_file.csv', 'w') as f:
            f.write('BOL123,Test Item,10,25.5\n')
        
        with open('test_file.csv', 'rb') as f:
            response = self.app.post('/upload', data={
                'file': f
            }, content_type='multipart/form-data')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('BOL123', data)
        self.assertEqual(data['BOL123']['name'], 'Test Item')
        self.assertEqual(data['BOL123']['quantity'], 10)
        self.assertEqual(data['BOL123']['price'], 25.5)

if __name__ == '__main__':
    unittest.main()
