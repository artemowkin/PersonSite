import datetime
import simplejson as json

from django.test import TestCase
from django.contrib.auth import get_user_model

from shop.models import Product, ProductReview
from .base import AllEndpointMixin, ConcreteEndpointMixin, BaseEndpointMixin


User = get_user_model()


def _product_setup(testcase):
	testcase.entry = testcase.model.objects.create(
		title='Some product', short_description='Some short description',
		description='Some description', price='100.00', amount=500,
	)
	testcase.serialized_entry = {
		'pk': str(testcase.entry.pk), 'image': None,
		'title': 'Some product',
		'short_description': 'Some short description',
		'description': 'Some description', 'price': '100.00',
		'amount': 500, 'available': True
	}


def _product_review_setup(testcase):
	testcase.user = User.objects.create_user(
		username='testuser', password='testpass'
	)
	testcase.product = testcase.product_model.objects.create(
		title='Some product', short_description='Some short description',
		description='Some description', price='100.00', amount=500,
	)
	testcase.review = testcase.review_model.objects.create(
		text='Review text', rating=5, author=testcase.user,
		product=testcase.product
	)
	testcase.serialized_review = {
		'pk': str(testcase.review.pk), 'text': 'Review text', 'rating': 5,
		'author': testcase.user.pk, 'product': str(testcase.product.pk),
		'pub_date': str(datetime.date.today())
	}


class AllProductsEndpointFunctionalTests(AllEndpointMixin, TestCase):
	"""Functional test for /shop/products/ endpoint"""

	endpoint = '/shop/products/'
	model = Product

	def setUp(self):
		super().setUp()
		_product_setup(self)

	def request_create_a_new_entry(self):
		"""Send POST request on /shop/products/"""
		return self.client.post(self.endpoint, {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}, content_type='application/json')

	def check_created_entry_fields(self, json_response):
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['title'], 'New product')
		self.assertEqual(
			json_response['short_description'], 'New short description'
		)
		self.assertEqual(json_response['description'], 'New description')
		self.assertEqual(json_response['price'], '200.00')
		self.assertEqual(json_response['amount'], 100)

	def test_create_a_new_product_with_existing_title(self):
		"""
		Test POST request on /shop/products/ endpoint with an
		existing title
		"""
		response =  self.client.post(self.endpoint, {
			'title': 'Some product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}, content_type='application/json')
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response, {
			'title': ['product with this product title already exists.']
		})


class ConcreteProductEndpointFunctionalTests(ConcreteEndpointMixin, TestCase):
	"""Functional tests for /shop/products/{product_pk}/ endpoint"""

	endpoint = '/shop/products/{product_pk}/'
	model = Product

	def setUp(self):
		super().setUp()
		_product_setup(self)
		self.updated_serialized_entry = self.serialized_entry.copy()
		self.updated_serialized_entry['title'] = 'New title'

	def get_request(self):
		return self.client.get(
			self.endpoint.format(product_pk=self.entry.pk)
		)

	def put_request(self):
		return self.client.put(
			self.endpoint.format(product_pk=self.entry.pk), {
				'title': 'New title',
				'short_description': 'Some short description',
				'description': 'Some description', 'price': '100.00',
				'amount': 500, 'available': True
			}, content_type='application/json'
		)

	def delete_request(self):
		return self.client.delete(
			self.endpoint.format(product_pk=self.entry.pk)
		)


class AllProductReviewsEndpointFunctionalTests(TestCase):
	"""Case of testing /shop/products/{product_pk}/reviews/ endpoint"""

	endpoint = '/shop/products/{product_pk}/reviews/'
	product_model = Product
	review_model = ProductReview

	def setUp(self):
		_product_review_setup(self)

	def test_get_all_product_reviews(self):
		response = self.client.get(
			self.endpoint.format(product_pk=str(self.product.pk))
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, {
			'overall_rating': 5.0, 'reviews': [self.serialized_review]
		})

	def test_create_a_new_product_review(self):
		response = self.client.post(
			self.endpoint.format(product_pk=str(self.product.pk)), {
				'text': 'New review', 'rating': 5
			}
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(self.product.reviews.count(), 2)
		self.assertIn('pk', json_response)
		self.assertEqual(json_response['text'], 'New review')
		self.assertEqual(json_response['rating'], 5)
