from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class BaseViewMixin:

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.client.login(username='testuser', password='testpass')


class AllCreateViewMixin(BaseViewMixin):

	def test_get(self):
		response = self.client.get(reverse(self.urlpattern))
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		response = self.client.post(
			reverse(self.urlpattern),
			self.post_request_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 201)


class ConcreteViewMixin(BaseViewMixin):

	def test_get(self):
		response = self.client.get(reverse(
			self.urlpattern, args=(str(self.entry.pk),)
		))
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		response = self.client.put(
			reverse(self.urlpattern, args=(str(self.entry.pk),)),
			self.put_request_data,
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)

	def test_delete(self):
		response = self.client.delete(reverse(
			self.urlpattern, args=(str(self.entry.pk),)
		))
		self.assertEqual(response.status_code, 204)
