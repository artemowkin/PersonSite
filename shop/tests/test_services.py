from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..models import Product
from ..services import (
	ProductsGetService, ProductCreateService, ProductUpdateService
)


User = get_user_model()


class ProductsGetServiceTests(TestCase):
	"""Case of testing ProductsGetService"""

	model = Product
	service = ProductsGetService()

	def setUp(self):
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)

	def test_get_concrete_with_correct_pk(self):
		"""Test does get_concrete() method return a concrete product"""
		product = self.service.get_concrete(self.product.pk)

		self.assertEqual(product, self.product)

	def test_get_concrete_with_incorrect_pk(self):
		"""
		Test does get_concrete() method with non-existing
		product pk raises Http404 extension
		"""
		with self.assertRaises(Http404):
			self.service.get_concrete(10)

	def test_get_all(self):
		"""Test does get_all() method return all products"""
		products = self.service.get_all()

		self.assertEqual(products.count(), 1)
		self.assertEqual(products[0], self.product)

	def test_get_all_doesnt_return_not_available_products(self):
		"""Test does get_all() not return not available products"""
		not_available_product = Product.objects.create(
			title='New product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
			available=False
		)
		products = self.service.get_all()

		self.assertEqual(products.count(), 1)
		self.assertEqual(products[0], self.product)


class ProductCreateServiceTests(TestCase):
	"""Case of testing ProductCreateService"""

	model = Product
	service = ProductCreateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product_data = {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}

	def test_create_with_superuser(self):
		"""
		Test does create() method requested by superuser
		creates a new product
		"""
		product = self.service.create(self.product_data, self.user)

		self.assertEqual(self.model.objects.count(), 1)
		self.assertEqual(product.title, 'New product')

	def test_create_with_simple_user(self):
		"""
		Test does create() method requested by simple user
		raises PermissionDenied exception
		"""
		simple_user = User.objects.create_user(
			username='simpleuser', password='simplepass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.create(self.product_data, simple_user)


class ProductUpdateServiceTests(TestCase):
	"""Case of testing PostUpdateService service"""

	model = Product
	service = ProductUpdateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.product_data = {
			'title': 'Edited product',
			'short_description': 'Some short description',
			'description': 'Some description', 'price': '100.00',
			'amount': 500, 'available': True
		}

	def test_update_with_correct_user(self):
		"""Test does update() method with correct user change the product"""
		product = self.service.update(
			self.product, self.product_data, self.user
		)

		self.assertEqual(product.title, 'Edited product')

	def test_update_without_available_in_data(self):
		"""
		Test does update() method without available field in
		data works correctly
		"""
		self.product_data.pop('available')
		product = self.service.update(
			self.product, self.product_data, self.user
		)

		self.assertEqual(product.title, 'Edited product')
		self.assertTrue(product.available)

	def test_update_with_incorrect_user(self):
		"""
		Test does update() method with incorrect user
		raises PermissionDenied exception
		"""
		bad_user = User.objects.create_user(
			username='baduser', password='badpass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.update(self.product, self.product_data, bad_user)
