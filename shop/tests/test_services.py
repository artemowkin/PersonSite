from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404

from generic.unit_tests import (
	GetServiceMixin, CreateServiceMixin, UpdateServiceMixin,
	DeleteServiceMixin
)
from ..models import Product
from ..services import (
	ProductsGetService, ProductCreateService, ProductUpdateService,
	ProductDeleteService
)


User = get_user_model()


class ProductsGetServiceTests(GetServiceMixin, TestCase):
	"""Case of testing ProductsGetService"""

	model = Product
	service = ProductsGetService()

	def setUp(self):
		self.entry = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)

	def test_get_all_doesnt_return_not_available_products(self):
		"""Test does get_all() not return not available products"""
		not_available_product = Product.objects.create(
			title='New product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
			available=False
		)
		products = self.service.get_all()

		self.assertEqual(products.count(), 1)
		self.assertEqual(products[0], self.entry)


class ProductCreateServiceTests(CreateServiceMixin, TestCase):
	"""Case of testing ProductCreateService"""

	model = Product
	service = ProductCreateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry_data = {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}

	def check_created_entry_fields(self, entry):
		self.assertEqual(entry.title, 'New product')
		self.assertEqual(entry.short_description, 'New short description')
		self.assertEqual(entry.description, 'New description')
		self.assertEqual(entry.price, '200.00')
		self.assertEqual(entry.amount, 100)


class ProductUpdateServiceTests(UpdateServiceMixin, TestCase):
	"""Case of testing PostUpdateService service"""

	model = Product
	service = ProductUpdateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.entry_data = {
			'title': 'Edited product',
			'short_description': 'Some short description',
			'description': 'Some description', 'price': '100.00',
			'amount': 500, 'available': True
		}

	def check_updated_entry_fields(self, entry):
		self.assertEqual(entry.title, 'Edited product')
		self.assertEqual(entry.short_description, 'Some short description')
		self.assertEqual(entry.description, 'Some description')
		self.assertEqual(entry.price, '100.00')
		self.assertEqual(entry.amount, 500)
		self.assertTrue(entry.available)

	def test_update_without_available_in_data(self):
		"""
		Test does update() method without available field in
		data works correctly
		"""
		self.entry_data.pop('available')
		product = self.service.update(
			self.entry, self.entry_data, self.user
		)

		self.check_updated_entry_fields(product)


class ProductDeleteServiceTests(DeleteServiceMixin, TestCase):
	"""Case of testing ProductDeleteService service"""

	model = Product
	service = ProductDeleteService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
