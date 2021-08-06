from django.urls import reverse

from generic.module_tests import BaseViewTest


class AllCreateProductsViewTests(BaseViewTest):
	"""Case of testing AllCreateProductsView"""

	urlpattern = 'all_products'

	def test_get(self):
		response = self.client.get(reverse(self.urlpattern))
		self.assertEqual(response.status_code, 200)
