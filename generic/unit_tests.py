from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.http import Http404


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


class GetServiceMixin:

	def test_get_concrete_with_correct_pk(self):
		entry = self.service.get_concrete(self.entry.pk)
		self.assertEqual(entry, self.entry)

	def test_get_concrete_with_incorrect_pk(self):
		with self.assertRaises(Http404):
			self.service.get_concrete(10)

	def test_get_all(self):
		entries = self.service.get_all()

		self.assertEqual(entries.count(), 1)
		self.assertEqual(entries[0], self.entry)


class CreateServiceMixin:

	def test_create(self):
		entry = self.service.create(self.entry_data, self.user)

		self.assertEqual(self.model.objects.count(), 1)
		self.check_created_entry_fields(entry)

	def test_create_with_simple_user(self):
		simple_user = User.objects.create_user(
			username='simpleuser', password='simplepass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.create(self.entry_data, simple_user)


class UpdateServiceMixin:

	def test_update_with_correct_user(self):
		entry = self.service.update(self.entry, self.entry_data, self.user)

		self.check_updated_entry_fields(entry)

	def test_update_with_incorrect_user(self):
		bad_user = User.objects.create_user(
			username='baduser', password='badpass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.update(self.entry, self.entry_data, bad_user)


class DeleteServiceMixin:

	def test_delete_with_correct_user(self):
		self.service.delete(self.entry, self.user)
		self.assertEqual(self.model.objects.count(), 0)

	def test_delete_with_incorrect_user(self):
		bad_user = User.objects.create_user(
			username='baduser', password='badpass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.delete(self.entry, bad_user)
