from django.urls import reverse
from django.contrib.auth import get_user_model

from generic.module_tests import BaseViewTest


User = get_user_model()


class AllCreateProductsViewTests(BaseViewTest):
	"""Case of testing AllCreateProductsView"""

	urlpattern = 'all_products'

	def test_get(self):
		response = self.client.get(reverse(self.urlpattern))
		self.assertEqual(response.status_code, 200)

	def test_post_with_superuser(self):
		response = self.client.post(reverse(self.urlpattern), {
			'title': 'New product',
			'short_description': 'New short description',
			'description': 'New description', 'price': '200.00',
			'amount': 100
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)
