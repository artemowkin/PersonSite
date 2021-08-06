from uuid import UUID

from django.test import TestCase

from ..models import Product


class ProductModelTests(TestCase):
	"""Case of testing Product model"""

	model = Product

	def setUp(self):
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)

	def test_model_entry_fields(self):
		"""Test are created model entry's fields valid"""
		self.assertIsInstance(self.product.pk, UUID)
		self.assertFalse(self.product.image)
		self.assertEqual(self.product.title, 'Some product')
		self.assertEqual(
			self.product.short_description, 'Some short description'
		)
		self.assertEqual(self.product.description, 'Some description')
		self.assertEqual(self.product.price, '100.00')
		self.assertEqual(self.product.amount, 500)
		self.assertTrue(self.product.available)

	def test_string_representation(self):
		"""Test is created model entry's string representation valid"""
		string_entry = str(self.product)

		self.assertEqual(string_entry, self.product.title)

	def test_absolute_url(self):
		"""Test does get_absolute_url() return a valid url"""
		# TODO: fix me
		pass
