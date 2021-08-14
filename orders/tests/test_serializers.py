from datetime import date
from uuid import uuid4

from django.test import TestCase

from ..serializers import OrderSerializer


class PostSerializerTests(TestCase):
	"""Case of testing PostSerializer"""

	serializer_class = OrderSerializer

	def setUp(self):
		self.serialized_order = {
			'pk': str(uuid4()), 'first_name': 'Ivan',
			'last_name': 'Ivanov', 'address': 'Pushkina, 25',
			'postal_code': '123456', 'city': 'Moscow', 'customer': {
				'pk': 1, 'username': 'testuser', 'email': 'testuser@gmail.com'
			},
			'status': 'processing'
		}

	def test_serializer_with_data_dict(self):
		"""Test is serializer valid with data dict"""
		serializer = self.serializer_class(data=self.serialized_order)

		self.assertTrue(serializer.is_valid())