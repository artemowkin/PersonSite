from uuid import UUID

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import Product, ProductReview


User = get_user_model()


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
		self.assertEqual(
			self.product.get_absolute_url(),
			reverse('concrete_product', args=[str(self.product.pk)])
		)


class ProductReviewModelTests(TestCase):
	"""Case of testing ProductReview model"""

	product_model = Product
	review_model = ProductReview

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.product = self.product_model.objects.create(
			title='Some product', short_description='Some short description',
			description='Some description', price='100.00', amount=500,
		)
		self.review = self.review_model.objects.create(
			text='Review text', rating=5, author=self.user,
			product=self.product
		)
		self.review.clean()

	def test_review_rating_min_value(self):
		"""Test does review.rating minimum value equal 1"""
		with self.assertRaises(ValidationError):
			self.review.rating = 0
			self.review.full_clean()

	def test_review_rating_max_value(self):
		"""Test does review.rating maximum value equal 5"""
		with self.assertRaises(ValidationError):
			self.review.rating = 6
			self.review.full_clean()

	def test_model_entry_fields(self):
		"""Test are created model entry's fields valid"""
		self.assertIsInstance(self.review.pk, UUID)
		self.assertEqual(self.review.text, 'Review text')
		self.assertEqual(self.review.rating, 5)
		self.assertEqual(self.review.author, self.user)
		self.assertEqual(self.review.product, self.product)

	def test_string_representation(self):
		"""Test is created model entry's string representation valid"""
		string_review = str(self.review)

		self.assertEqual(
			string_review, (
				f"{self.review.product.title} review "
				f"from {self.review.author.username}"
			)
		)

	def test_absolute_url(self):
		"""Test does get_absolute_url() return a valid url"""
		self.assertEqual(
			self.review.get_absolute_url(),
			reverse('concrete_product_review', args=[
				str(self.product.pk), str(self.review.pk)
			])
		)
