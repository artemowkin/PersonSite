from django.test import TestCase

from generic.unit_tests import AllCreateViewMixin, ConcreteViewMixin
from ..models import Product


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
