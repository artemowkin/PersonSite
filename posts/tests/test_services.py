from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import Http404
from django.core.exceptions import PermissionDenied

from ..models import Post
from ..services import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)


User = get_user_model()


class PostGetServiceTests(TestCase):
	"""Case of testing PostGetService service"""

	model = Post
	service = PostGetService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = self.model.objects.create(
			title='Some post', text='Some text', author=self.user
		)

	def test_get_concrete_with_correct_pk(self):
		"""Test does get_concrete() method return a concrete post"""
		post = self.service.get_concrete(self.post.pk)

		self.assertEqual(post, self.post)

	def test_get_concrete_with_incorrect_pk(self):
		"""
		Test does get_concrete() method with non-existing
		post pk raises Http404 extension
		"""
		with self.assertRaises(Http404):
			self.service.get_concrete(10)

	def test_get_all(self):
		"""Test does get_all() method return all posts entries"""
		posts = self.service.get_all()

		self.assertEqual(posts.count(), 1)
		self.assertEqual(posts[0], self.post)

	def test_get_user_posts(self):
		"""Test does get_user_posts() method return correct data"""
		posts = self.service.get_user_posts(self.user.pk)

		self.assertEqual(posts.count(), 1)
		self.assertEqual(posts[0], self.post)

	def test_get_user_posts_with_random_user(self):
		"""Test does get_user_posts() with random user return no data"""
		posts = self.service.get_user_posts(10)

		self.assertEqual(posts.count(), 0)


class PostCreateServiceTests(TestCase):
	"""Case of testing PostCreateService service"""

	model = Post
	service = PostCreateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post_data = {'title': 'Some post', 'text': 'Some text'}

	def test_create(self):
		"""Test does create() method creates a new post entry"""
		post = self.service.create(self.post_data, self.user)

		self.assertEqual(self.model.objects.count(), 1)
		self.assertEqual(post.title, 'Some post')
		self.assertEqual(post.text, 'Some text')


class PostUpdateServiceTests(TestCase):
	"""Case of testing PostUpdateService service"""

	model = Post
	service = PostUpdateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = self.model.objects.create(
			title='Some post', text='Some text', author=self.user
		)
		self.post_data = {'title': 'Edited post', 'text': 'Some text'}

	def test_update_with_correct_user(self):
		"""Test does update() method with correct user change the post"""
		post = self.service.update(self.post, self.post_data, self.user)

		self.assertEqual(post.title, 'Edited post')
		self.assertEqual(post.text, 'Some text')

	def test_update_with_incorrect_user(self):
		"""
		Test does update() method with incorrect user
		raises PermissionDenied exception
		"""
		bad_user = User.objects.create_superuser(
			username='baduser', password='badpass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.update(self.post, self.post_data, bad_user)


class PostDeleteServiceTests(TestCase):
	"""Case of testing PostDeleteService service"""

	model = Post
	service = PostDeleteService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = self.model.objects.create(
			title='Some post', text='Some text', author=self.user
		)

	def test_delete_with_correct_user(self):
		"""Test does delete() method delete the post if user is correct"""
		self.service.delete(self.post, self.user)

		self.assertEqual(self.model.objects.count(), 0)

	def test_delete_with_incorrect_user(self):
		"""
		Test does delete() method raise PermissionDenied exception
		if user is incorrect
		"""
		bad_user = User.objects.create_superuser(
			username='baduser', password='badpass'
		)
		with self.assertRaises(PermissionDenied):
			self.service.delete(self.post, bad_user)
