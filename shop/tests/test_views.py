from django.urls import reverse
from django.contrib.auth import get_user_model

from generic.module_tests import BaseViewTest
from ..models import Product


User = get_user_model()


class AllCreateProductsViewTests(BaseViewTest):
	"""Case of testing AllCreateProductsView"""

	urlpattern = 'all_products'

	def test_get(self):
		response = self.client.get(reverse(self.urlpattern))
		self.assertEqual(response.status_code, 200)

	def test_post_with_superuser(self):
		response = self.client.post(reverse(self.urlpattern), {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)


class ConcreteProductViewTests(BaseViewTest):
	"""Case of testing ConcretePostView view"""

	model = Product
	urlpattern = 'concrete_product'

	def setUp(self):
		super().setUp()
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)

	def test_get(self):
		"""Test does GET request return 200 response"""
		response = self.client.get(reverse(
			self.urlpattern, args=(str(self.product.pk),)
		))
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		"""Test does PUT request return 200 response"""
		response = self.client.put(
			reverse(self.urlpattern, args=(str(self.product.pk),)), {
				'title': 'New product',
				'short_description': 'New short description',
				'description': 'New description', 'price': '200.00',
				'amount': 100
			}, content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)
