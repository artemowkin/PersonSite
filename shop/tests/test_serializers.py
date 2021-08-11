import datetime
from uuid import uuid4

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..serializers import ProductSerializer, ProductReviewSerializer
from ..models import Product


User = get_user_model()


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


class ProductReviewSerializerTests(TestCase):
	"""Case of testing ProductReviewSerializer"""

	serializer_class = ProductReviewSerializer

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.serialized_product_review = {
			'text': 'Some review', 'rating': 5, 'author': {
				'pk': self.user.pk,
				'username': self.user.username,
				'email': self.user.email,
			},
			'product': str(self.product.pk),
			'pub_date': str(datetime.date.today())
		}

	def test_serializer_with_data_dict(self):
		"""Test is serializer valid with data dict"""
		serializer = self.serializer_class(data=self.serialized_product_review)

		self.assertTrue(serializer.is_valid())

	def test_serializer_rating_min_value(self):
		self.serialized_product_review['rating'] = 0
		serializer = self.serializer_class(data=self.serialized_product_review)

		self.assertFalse(serializer.is_valid())

	def test_serializer_rating_max_value(self):
		self.serialized_product_review['rating'] = 6
		serializer = self.serializer_class(data=self.serialized_product_review)

		self.assertFalse(serializer.is_valid())
