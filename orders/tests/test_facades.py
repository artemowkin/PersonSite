from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services.facades import OrderGetFacade, OrderCreateFacade
from ..models import Order
from ..serializers import OrderSerializer


User = get_user_model()


class OrderGetFacadeTests(TestCase):
	"""Case of testing OrderGetFacade"""

	def setUp(self):
		self.user = User.objects.create_user(
			username='testuser', password='testpass'
		)
		self.order = Order.objects.create(
			first_name='Ivan', last_name='Ivanov', address='Pushkina, 25',
			postal_code='123456', city='Moscow', customer=self.user
		)
		self.serialized_order = OrderSerializer(self.order).data
		self.facade = OrderGetFacade(self.user)

	def test_get_concrete(self):
		order, status_code = self.facade.get_concrete(self.order.pk)

		self.assertEqual(order, self.serialized_order)
		self.assertEqual(status_code, 200)

	def test_get_all(self):
		orders, status_code = self.facade.get_all()

		self.assertEqual(orders, [self.serialized_order])
		self.assertEqual(status_code, 200)


class OrderCreateFacadeTests(TestCase):
	"""Case of testing OrderCreateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.order_data = {
			'first_name': 'Ivan', 'last_name': 'Ivanov',
			'address': 'Pushkina, 25', 'postal_code': '123456',
			'city': 'Moscow'
		}
		self.facade = OrderCreateFacade()

	def test_create(self):
		order, status_code = self.facade.create(self.order_data, self.user)

		self.assertIn('pk', order)
		self.assertEqual(order['first_name'], 'Ivan')
		self.assertEqual(order['last_name'], 'Ivanov')
		self.assertEqual(order['address'], 'Pushkina, 25')
		self.assertEqual(order['postal_code'], '123456')
		self.assertEqual(order['city'], 'Moscow')
		self.assertEqual(status_code, 201)
