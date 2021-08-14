import datetime
import simplejson as json

from django.test import TestCase

from orders.models import Order
from .base import AllEndpointMixin, ConcreteEndpointMixin


def _order_setup(testcase):
	testcase.entry = testcase.model.objects.create(
		first_name='Ivan', last_name='Ivanov', address='Pushkina, 25',
		postal_code='123456', city='Moscow', customer=testcase.user
	)
	testcase.serialized_entry = {
		'pk': str(testcase.entry.pk), 'first_name': 'Ivan',
		'last_name': 'Ivanov', 'address': 'Pushkina, 25',
		'postal_code': '123456', 'city': 'Moscow', 'customer': {
			'pk': testcase.user.pk, 'username': testcase.user.username,
			'email': testcase.user.email
		}, 'status': 'processing', 'pub_date': str(datetime.date.today())
	}


class AllOrdersEndpointFunctionalTests(AllEndpointMixin, TestCase):
	"""Functional tests for /shop/orders/ endpoint"""

	endpoint = '/shop/orders/'
	model = Order

	def setUp(self):
		super().setUp()
		_order_setup(self)

	def request_create_a_new_entry(self):
		"""Test POST request on /posts/ endpoint"""
		return self.client.post(self.endpoint, {
			'first_name': 'Ivan', 'last_name': 'Ivanov',
			'address': 'Pushkina, 25', 'postal_code': '123456',
			'city': 'Moscow'
		}, content_type='application/json')

	def check_created_entry_fields(self, json_response):
		self.assertIn('pk', json_response)
		self.assertIn('first_name', json_response)
		self.assertIn('last_name', json_response)
		self.assertIn('address', json_response)
		self.assertIn('postal_code', json_response)
		self.assertIn('city', json_response)
		self.assertIn('status', json_response)
		self.assertIn('pub_date', json_response)

	def test_get_entries_with_not_authenticated_user(self):
		self.client.logout()
		response = self.client.get(self.endpoint)

		self.assertEqual(response.status_code, 403)

	def test_create_a_new_entry_with_not_authenticated_user(self):
		self.client.logout()
		response = self.request_create_a_new_entry()

		self.assertEqual(response.status_code, 403)
