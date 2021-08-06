from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class BaseViewTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.client.login(username='testuser', password='testpass')
