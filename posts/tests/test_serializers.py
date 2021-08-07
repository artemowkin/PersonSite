from datetime import date
from uuid import uuid4

from django.test import TestCase

from ..serializers import PostSerializer


class PostSerializerTests(TestCase):
	"""Case of testing PostSerializer"""

	serializer_class = PostSerializer

	def setUp(self):
		self.serialized_post = {
			'pk': uuid4(), 'title': 'Some post', 'text': 'Some text',
			'preview': None, 'pub_date': str(date.today())
		}

	def test_serializer_with_data_dict(self):
		"""Test is serializer valid with data dict"""
		serializer = self.serializer_class(data=self.serialized_post)

		self.assertTrue(serializer.is_valid())
