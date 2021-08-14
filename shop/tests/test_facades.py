from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services.facades import (
	ProductGetFacade, ProductCreateFacade, ProductUpdateFacade,
	ProductDeleteFacade, ProductReviewGetFacade, ProductReviewCreateFacade,
	ProductReviewUpdateFacade, ProductReviewDeleteFacade
)
from ..models import Product, ProductReview
from ..serializers import ProductSerializer, ProductReviewSerializer


User = get_user_model()


class ProductGetFacadeTests(TestCase):
	"""Case of testing ProductGetFacade"""

	def setUp(self):
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.serialized_product = ProductSerializer(self.product).data
		self.facade = ProductGetFacade()

	def test_get_concrete(self):
		product, status_code = self.facade.get_concrete(self.product.pk)

		self.assertEqual(product, self.serialized_product)
		self.assertEqual(status_code, 200)

	def test_get_all(self):
		products, status_code = self.facade.get_all()

		self.assertEqual(products, [self.serialized_product])
		self.assertEqual(status_code, 200)


class ProductCreateFacadeTests(TestCase):
	"""Case of testing ProductCreateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product_data = {
			'title': 'Some product',
			'short_description': 'Some short description',
			'description': 'Some description', 'price': '100.00', 'amount': 500
		}
		self.facade = ProductCreateFacade()

	def test_create(self):
		product, status_code = self.facade.create(self.product_data, self.user)

		self.assertIn('pk', product)
		self.assertEqual(product['title'], 'Some product')
		self.assertEqual(product['short_description'], 'Some short description')
		self.assertEqual(product['description'], 'Some description')
		self.assertEqual(product['price'], '100.00')
		self.assertEqual(product['amount'], 500)
		self.assertEqual(status_code, 201)


class ProductUpdateFacadeTests(TestCase):
	"""Case of testing ProductUpdateFacade"""

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
			'description': 'Some description', 'price': '100.00', 'amount': 500
		}
		self.facade = ProductUpdateFacade()

	def test_update(self):
		product, status_code = self.facade.update(
			self.product.pk, self.product_data, self.user
		)

		self.assertEqual(product['title'], 'Edited product')
		self.assertEqual(product['short_description'], 'Some short description')
		self.assertEqual(product['description'], 'Some description')
		self.assertEqual(product['price'], '100.00')
		self.assertEqual(product['amount'], 500)
		self.assertEqual(status_code, 200)


class ProductDeleteFacadeTests(TestCase):
	"""Case of testing ProductDeleteFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.facade = ProductDeleteFacade()

	def test_delete(self):
		data, status_code = self.facade.delete(self.product.pk, self.user)

		self.assertIsNone(data)
		self.assertEqual(status_code, 204)


class ProductReviewGetFacadeTests(TestCase):
	"""Case of testing ProductReviewGetFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = ProductReview.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.serialized_review = ProductReviewSerializer(self.review).data
		self.facade = ProductReviewGetFacade(self.product.pk)

	def test_get_concrete(self):
		review, status_code = self.facade.get_concrete(self.review.pk)

		self.assertEqual(review, self.serialized_review)
		self.assertEqual(status_code, 200)

	def test_get_all(self):
		reviews, status_code = self.facade.get_all()

		self.assertEqual(reviews, {
			'overall_rating': 5.0, 'reviews': [self.serialized_review]
		})
		self.assertEqual(status_code, 200)


class ProductReviewCreateFacadeTests(TestCase):
	"""Case of testing ProductReviewCreateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review_data = {
			'text': 'Review text', 'rating': 5
		}
		self.facade = ProductReviewCreateFacade(self.product.pk)

	def test_create(self):
		review, status_code = self.facade.create(self.review_data, self.user)

		self.assertIn('pk', review)
		self.assertEqual(review['text'], 'Review text')
		self.assertEqual(review['rating'], 5)
		self.assertEqual(status_code, 201)


class ProductReviewUpdateFacadeTests(TestCase):
	"""Case of testing ProductReviewUpdateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = ProductReview.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.review_data = {
			'text': 'Edited review', 'rating': 5
		}
		self.facade = ProductReviewUpdateFacade(self.product.pk)

	def test_update(self):
		review, status_code = self.facade.update(
			self.review.pk, self.review_data, self.user
		)

		self.assertEqual(review['text'], 'Edited review')
		self.assertEqual(review['rating'], 5)
		self.assertEqual(status_code, 200)


class ProductReviewDeleteFacadeTests(TestCase):
	"""Case of testing ProductReviewDeleteFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = Product.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = ProductReview.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.facade = ProductReviewDeleteFacade(self.product.pk)

	def test_delete(self):
		data, status_code = self.facade.delete(self.review.pk, self.user)

		self.assertIsNone(data)
		self.assertEqual(status_code, 204)
