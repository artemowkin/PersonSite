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
