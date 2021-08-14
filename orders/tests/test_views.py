from django.test import TestCase

from generic.unit_tests import AllCreateViewMixin


class AllCreateOrdersViewTests(AllCreateViewMixin, TestCase):
	"""Case of testing AllCreateOrdersView view"""

	urlpattern = 'all_orders'

	def setUp(self):
		super().setUp()
		self.post_request_data = {
			'first_name': 'Ivan', 'last_name': 'Ivanov',
			'address': 'Pushkina, 25', 'postal_code': '123456',
			'city': 'Moscow'
		}
