from django.test import TestCase
from django.urls import reverse

from generic.unit_tests import (
	AllCreateViewMixin, ConcreteViewMixin, BaseViewMixin
)
from ..models import Product, ProductReview


class AllCreateProductsViewTests(AllCreateViewMixin, TestCase):
	"""Case of testing AllCreateProductsView"""

	urlpattern = 'all_products'

	def setUp(self):
		super().setUp()
		self.post_request_data = {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}


class ConcreteProductViewTests(ConcreteViewMixin, TestCase):
	"""Case of testing ConcretePostView view"""

	model = Product
	urlpattern = 'concrete_product'

	def setUp(self):
		super().setUp()
		self.entry = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.put_request_data = {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}


class AllProductReviewsViewTests(BaseViewMixin, TestCase):
	"""Case of testing AllProductReviewsView"""

	urlpattern = 'all_product_reviews'
	product_model = Product
	review_model = ProductReview

	def setUp(self):
		super().setUp()
		self.product = self.product_model.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = self.review_model.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.review_data = {'text': 'New review', 'rating': 5}

	def test_get(self):
		response = self.client.get(
			reverse(self.urlpattern, args=[str(self.product.pk)])
		)
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		response = self.client.post(
			reverse(self.urlpattern, args=[str(self.product.pk)]), 
			self.review_data, content_type='application/json'
		)
		self.assertEqual(response.status_code, 201)


class ConcreteProductReviewViewTests(BaseViewMixin, TestCase):
	"""Case of testing ConcreteProductReviewView"""

	urlpattern = 'concrete_product_review'
	product_model = Product
	review_model = ProductReview

	def setUp(self):
		super().setUp()
		self.product = self.product_model.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = self.review_model.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.review_data = {'text': 'Updated review', 'rating': 5}

	def test_get(self):
		response = self.client.get(
			reverse(self.urlpattern, args=[
				str(self.product.pk), str(self.review.pk)
			])
		)
		self.assertEqual(response.status_code, 200)
