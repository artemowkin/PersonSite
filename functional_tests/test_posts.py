import simplejson as json

from django.test import TestCase

from posts.models import Post
from .base import AllEndpointMixin, ConcreteEndpointMixin


def _post_setup(testcase):
	testcase.entry = testcase.model.objects.create(
		title='Post title', text='Post text'
	)
	testcase.serialized_entry = {
		'pk': str(testcase.entry.pk), 'title': 'Post title',
		'text': 'Post text', 'preview': None,
		'pub_date': str(testcase.entry.pub_date)
	}


class AllPostsEndpointFunctionalTests(AllEndpointMixin, TestCase):
	"""Functional tests for /posts/ endpoint"""

	endpoint = '/posts/'
	model = Post

	def setUp(self):
		super().setUp()
		_post_setup(self)

	def request_create_a_new_entry(self):
		"""Test POST request on /posts/ endpoint"""
		return self.client.post(self.endpoint, {
			'title': 'New post', 'text': 'New post text'
		}, content_type='application/json')

	def check_created_entry_fields(self, json_response):
		self.assertIn('pk', json_response)
		self.assertIn('title', json_response)
		self.assertIn('text', json_response)

	def test_create_a_new_post_with_existing_title(self):
		"""Test POST request on /posts/ endpoint with an existing title"""
		response = self.client.post(self.endpoint, {
			'title': 'Post title', 'text': 'Post text'
		}, content_type='application/json')
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response, {
			'title': ['post with this post title already exists.']
		})

	def test_create_a_new_entry_with_not_superuser(self):
		"""
		Test does POST on /posts/ with not a superuser
		return 403 response
		"""
		new_user = User.objects.create_user(
			username='justuser', password='pass'
		)
		self.client.login(username='justuser', password='pass')
		response = self.request_create_a_new_entry()

		self.assertEqual(response.status_code, 403)


class ConcretePostEndpointFunctionalTests(ConcreteEndpointMixin, TestCase):
	"""Functional tests for /posts/{post_pk}/ endpoint"""

	endpoint = '/posts/{post_pk}/'
	model = Post
	def setUp(self):
		super().setUp()
		_post_setup(self)
		self.updated_serialized_entry = self.serialized_entry.copy()
		self.updated_serialized_entry['title'] = 'New title'

	def get_request(self):
		return self.client.get(
			self.endpoint.format(post_pk=self.entry.pk)
		)

	def put_request(self):
		return self.client.put(
			self.endpoint.format(post_pk=self.entry.pk), {
				'title': 'New title', 'text': 'Post text'
			}, content_type='application/json'
		)

	def delete_request(self):
		return self.client.delete(
			self.endpoint.format(post_pk=self.entry.pk)
		)
