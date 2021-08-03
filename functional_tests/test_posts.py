import simplejson as json

from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post


User = get_user_model()


class BasePostFunctionalTest(TestCase):
	"""Base functional test for posts endpoints"""

	model = Post

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass',
			email='testuser@gmail.com'
		)
		self.client.login(username='testuser', password='testpass')
		self.post = self.model.objects.create(
			title='Post title', text='Post text', author=self.user
		)
		self.serialized_post = {
			'pk': str(self.post.pk), 'title': 'Post title',
			'text': 'Post text', 'preview': None, 'author': {
				'pk': self.user.pk, 'username': 'testuser',
				'email': 'testuser@gmail.com'
			},
			'pub_date': str(self.post.pub_date)
		}


class AllPostsEndpointFunctionalTests(BasePostFunctionalTest):
	"""Functional tests for /posts/ endpoint"""

	endpoint = '/posts/'

	def test_get_all_posts(self):
		"""Test GET request on /posts/ endpoint"""
		response = self.client.get(self.endpoint)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, [self.serialized_post])

	def test_create_a_new_post(self):
		"""Test POST request on /posts/ endpoint"""
		response = self.client.post(self.endpoint, {
			'title': 'New post', 'text': 'New post text'
		}, content_type='application/json')
		json_response = json.loads(response.content)
		posts_entries_count = self.model.objects.count()

		self.assertEqual(response.status_code, 201)
		self.assertIn('pk', json_response)
		self.assertIn('title', json_response)
		self.assertIn('text', json_response)
		self.assertEqual(posts_entries_count, 2)

	def test_create_a_new_post_with_incorrect_data(self):
		"""Test POST request on /posts/ endpoint with incorrect data"""
		response = self.client.post(self.endpoint, {
			'incorrect': 'data'
		}, content_type='application/json')
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response, {
			'title': ['This field is required.'],
			'text': ['This field is required.']
		})

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


class ConcretePostEndpointFunctionalTests(BasePostFunctionalTest):
	"""Functional tests for /posts/{post_pk}/ endpoint"""

	endpoint = '/posts/{post_pk}/'

	def test_get_a_concrete_post(self):
		"""Test GET request on /posts/{post_pk}/ endpoint"""
		response = self.client.get(
			self.endpoint.format(post_pk=self.post.pk)
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, self.serialized_post)

	def put_request(self):
		"""Request PUT on /posts/{post_pk}/ endpoint"""
		return self.client.put(
			self.endpoint.format(post_pk=self.post.pk), {
				'title': 'Edited title', 'text': 'Edited text'
			}, content_type='application/json'
		)

	def bad_login(self):
		"""Login the bad user"""
		bad_user = User.objects.create_superuser(
			username='baduser', password='badpass'
		)
		self.client.login(username='baduser', password='badpass')

	def test_update_a_concrete_post(self):
		"""
		Test PUT request on /posts/{post_pk}/ endpoint with
		correct user
		"""
		response = self.put_request()
		json_response = json.loads(response.content)
		self.serialized_post['title'] = 'Edited title'
		self.serialized_post['text'] = 'Edited text'

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, self.serialized_post)

	def test_update_a_concrete_post_with_bad_user(self):
		"""
		Test PUT request on /posts/{post_pk}/ endpoint with
		incorrect user
		"""
		self.bad_login()
		response = self.put_request()
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 403)
		self.assertEqual(json_response, {
			'detail': 'You do not have permission to perform this action.'
		})

	def test_update_a_concrete_post_with_incorrect_data(self):
		"""
		Test POST request on /posts/{post_pk}/ endpoint with
		incorrect data
		"""
		response = self.client.put(
			self.endpoint.format(post_pk=self.post.pk), {
				'incorrect': 'data'
			}, content_type='application/json'
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(json_response, {
			'title': ['This field is required.'],
			'text': ['This field is required.']
		})

	def delete_request(self):
		"""Request DELETE on /posts/{post_pk}/ endpoint"""
		return self.client.delete(
			self.endpoint.format(post_pk=self.post.pk)
		)

	def test_delete_a_concrete_post(self):
		"""
		Test DELETE request on /posts/{post_pk}/ endpoint with
		correct user
		"""
		response = self.delete_request()
		posts_entries_count = Post.objects.count()

		self.assertEqual(response.status_code, 204)
		self.assertEqual(posts_entries_count, 0)

	def test_delete_a_concrete_post_with_bad_user(self):
		"""
		Test DELETE request on /posts/{post_pk}/ endpoint with
		incorrect user
		"""
		self.bad_login()
		response = self.delete_request()
		posts_entries_count = Post.objects.count()

		self.assertEqual(response.status_code, 403)
		self.assertEqual(posts_entries_count, 1)


class UserPostsEndpointFunctionalTests(BasePostFunctionalTest):
	"""Functional tests for /posts/users/{user_pk}/ endpoint"""

	endpoint = '/posts/user/{user_pk}/'

	def test_get_correct_user_posts(self):
		"""
		Test GET request on /posts/user/{user_pk}/ endpoint with
		current user
		"""
		response = self.client.get(
			self.endpoint.format(user_pk=self.user.pk)
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(json_response, [self.serialized_post])
		self.assertEqual(json_response[0]['author']['pk'], self.user.pk)

	def test_get_incorrect_user_posts(self):
		"""
		Test GET request on /posts/user/{user_pk}/ endpoint with
		non-existent user_pk
		"""
		response = self.client.get(
			self.endpoint.format(user_pk=5)
		)
		json_response = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(json_response), 0)
