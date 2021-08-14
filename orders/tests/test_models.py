from uuid import UUID

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from ..models import Order


User = get_user_model()


class OrderModelTests(TestCase):
	"""Case of testing Order model"""

	model = Order

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.order = self.model.objects.create(
			first_name='Ivan', last_name='Ivanov', address='Pushkina, 25',
			postal_code='123456', city='Moscow', customer=self.user
		)

	def test_model_entry_fields(self):
		"""Test are created model entry's fields valid"""
		self.assertIsInstance(self.order.pk, UUID)
		self.assertEqual(self.order.first_name, 'Ivan')
		self.assertEqual(self.order.last_name, 'Ivanov')
		self.assertEqual(self.order.address, 'Pushkina, 25')
		self.assertEqual(self.order.postal_code, '123456')
		self.assertEqual(self.order.city, 'Moscow')
		self.assertEqual(self.order.customer, self.user)
		self.assertEqual(self.order.status, 'processing')

	def test_string_representation(self):
		"""Test is created model entry's string representation valid"""
		string_entry = str(self.order)

		self.assertEqual(
			string_entry, (
				f"{self.order.first_name} {self.order.last_name}"
				f" ({self.order.city})"
			)
		)

	def test_absolute_url(self):
		"""Test does get_absolute_url() return a valid url"""
		# TODO: FixMe
		pass
