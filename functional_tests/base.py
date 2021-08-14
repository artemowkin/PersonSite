import simplejson as json

from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseEndpointMixin:
	"""Base mixin with default setup"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass',
			email='testuser@gmail.com'
		)
		self.client.login(username='testuser', password='testpass')


class AllEndpointMixin(BaseEndpointMixin):
	"""
	Functional test mixin for endpoint to get all entries and
	create a new entry
	"""

	def test_get_all_entries(self):
		response = self.client.get(self.endpoint)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, [self.serialized_entry])

	def request_create_a_new_entry(self):
		raise NotImplementedError

	def check_created_entry_fields(self, json_response):
		raise NotImplementedError

	def test_create_a_new_entry(self):
		response = self.request_create_a_new_entry()
		json_response = json.loads(response.content)
		entries_count = self.model.objects.count()

		self.assertEqual(response.status_code, 201)
		self.check_created_entry_fields(json_response)
		self.assertEqual(entries_count, 2)


class ConcreteEndpointMixin(BaseEndpointMixin):
	"""
	Functional test mixin for endpoint to get a concrete entry,
	update it, and delete it
	"""

	def get_request(self):
		raise NotImplementedError

	def put_request(self):
		raise NotImplementedError

	def delete_request(self):
		raise NotImplementedError

	def test_get_a_concrete_entry(self):
		response = self.get_request()
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, self.serialized_entry)

	def bad_login(self):
		"""Login the bad user"""
		bad_user = User.objects.create_user(
			username='baduser', password='badpass'
		)
		self.client.login(username='baduser', password='badpass')

	def test_update_a_concrete_entry(self):
		response = self.put_request()
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, self.updated_serialized_entry)

	def test_update_a_concrete_entry_with_bad_user(self):
		self.bad_login()
		response = self.put_request()
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 403)
		self.assertEqual(json_response, {
			'detail': 'You do not have permission to perform this action.'
		})

	def test_delete_a_concrete_entry(self):
		response = self.delete_request()
		entries_count = self.model.objects.count()

		self.assertEqual(response.status_code, 204)
		self.assertEqual(entries_count, 0)

	def test_delete_a_concrete_entry_with_bad_user(self):
		self.bad_login()
		response = self.delete_request()
		entries_count = self.model.objects.count()

		self.assertEqual(response.status_code, 403)
		self.assertEqual(entries_count, 1)
