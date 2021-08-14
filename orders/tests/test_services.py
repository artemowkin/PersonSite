from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from generic.unit_tests import GetServiceMixin
from ..models import Order
from ..services.base import OrderGetService, OrderCreateService


User = get_user_model()


class OrderGetServiceTests(GetServiceMixin, TestCase):
	"""Case of testing OrderGetService service"""

	model = Order

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = self.model.objects.create(
			first_name='Ivan', last_name='Ivanov', address='Pushkina, 25',
			postal_code='123456', city='Moscow', customer=self.user
		)
		self.service = OrderGetService(self.user)


class OrderCreateServiceTests(TestCase):
	"""Case of testing OrderCreateService service"""

	model = Order

	def setUp(self):
		self.user = User.objects.create_user(
			username='testuser', password='testpass'
		)
		self.service = OrderCreateService()
		self.order_data = {
			'first_name': 'Ivan', 'last_name': 'Ivanov',
			'address': 'Pushkina, 25', 'postal_code': '123456',
			'city': 'Moscow'
		}

	def test_create(self):
		order = self.service.create(self.order_data, self.user)

		self.assertEqual(self.model.objects.count(), 1)
		self.assertEqual(order.first_name, 'Ivan')
		self.assertEqual(order.last_name, 'Ivanov')
		self.assertEqual(order.address, 'Pushkina, 25')
		self.assertEqual(order.postal_code, '123456')
		self.assertEqual(order.city, 'Moscow')
		self.assertEqual(order.customer, self.user)

	def test_create_with_not_authenticated_user(self):
		anon = AnonymousUser()
		with self.assertRaises(PermissionDenied):
			self.service.create(self.order_data, anon)
