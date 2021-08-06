from uuid import uuid4

from django.test import TestCase

from ..serializers import ProductSerializer


class ProductSerializerTests(TestCase):
	"""Case of testing ProductSerializer"""

	serializer_class = ProductSerializer

	def setUp(self):
		self.serialized_product = {
			'pk': uuid4(), 'image': None,
			'title': 'Some product',
			'short_description': 'Some short description',
			'description': 'Some description', 'price': 100.0,
			'amount': 500, 'available': True
		}

	def test_serializer_with_data_dict(self):
		"""Test is serializer valid with data dict"""
		serializer = self.serializer_class(data=self.serialized_product)

		self.assertTrue(serializer.is_valid())
