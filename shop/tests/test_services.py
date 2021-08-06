from django.test import TestCase

from ..models import Product
from ..services import ProductsGetService


class ProductsGetServiceTests(TestCase):
	"""Case of testing ProductsGetService"""

	model = Product
	service = ProductsGetService()

	def setUp(self):
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)

	def test_get_all(self):
		"""Test does get_all() method return all products"""
		products = self.service.get_all()

		self.assertEqual(products.count(), 1)
		self.assertEqual(products[0], self.product)

	def test_get_all_doesnt_return_not_available_products(self):
		"""Test does get_all() not return not available products"""
		not_available_product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
			available=False
		)
		products = self.service.get_all()

		self.assertEqual(products.count(), 1)
		self.assertEqual(products[0], self.product)
