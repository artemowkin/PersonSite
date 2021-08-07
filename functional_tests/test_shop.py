import simplejson as json

from django.contrib.auth import get_user_model
from django.test import TestCase

from shop.models import Product


User = get_user_model()


class BaseProductsFunctionalTest(TestCase):
	"""Base functional test for products endpoints"""

	model = Product

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass',
			email='example@gmail.com'
		)
		self.client.login(username='testuser', password='testpass')
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.serialized_product = {
			'pk': str(self.product.pk), 'image': None,
			'title': 'Some product',
			'short_description': 'Some short description',
			'description': 'Some description', 'price': '100.00',
			'amount': 500, 'available': True
		}


class AllProductsEndpointFunctionalTests(BaseProductsFunctionalTest):
	"""Functional test for /shop/products/ endpoint"""

	endpoint = '/shop/products/'

	def test_get_all_products(self):
		response = self.client.get(self.endpoint)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, [self.serialized_product])

	def _request_create_a_new_product(self):
		"""Send POST request on /shop/products/"""
		return self.client.post(self.endpoint, {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}, content_type='application/json')

	def test_create_a_new_product(self):
		response = self._request_create_a_new_product()
		json_response = json.loads(response.content)
		products_count = self.model.objects.count()

		self.assertEqual(response.status_code, 201)
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['title'], 'New product')
		self.assertEqual(
			json_response['short_description'], 'New short description'
		)
		self.assertEqual(json_response['description'], 'New description')
		self.assertEqual(json_response['price'], '200.00')
		self.assertEqual(json_response['amount'], 100)
		self.assertEqual(products_count, 2)

	def test_create_a_new_product_with_not_superuser(self):
		"""
		Test does POST on /shop/products/ with not a superuser
		return 403 response
		"""
		new_user = User.objects.create_user(
			username='justuser', password='pass'
		)
		self.client.login(username='justuser', password='pass')
		response = self._request_create_a_new_product()

		self.assertEqual(response.status_code, 403)
