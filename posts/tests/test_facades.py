from django.test import TestCase
from django.contrib.auth import get_user_model

from ..services.facades import (
	PostGetFacade, PostCreateFacade, PostUpdateFacade, PostDeleteFacade
)
from ..models import Post
from ..serializers import PostSerializer


User = get_user_model()


class PostGetFacadeTests(TestCase):
	"""Case of testing PostGetFacade"""

	def setUp(self):
		self.post = Post.objects.create(
			title='Some post', text='Some text'
		)
		self.serialized_post = PostSerializer(self.post).data
		self.facade = PostGetFacade()

	def test_get_concrete(self):
		post, status_code = self.facade.get_concrete(self.post.pk)

		self.assertEqual(post, self.serialized_post)
		self.assertEqual(status_code, 200)

	def test_get_all(self):
		posts, status_code = self.facade.get_all()

		self.assertEqual(posts, [self.serialized_post])
		self.assertEqual(status_code, 200)


class PostCreateFacadeTests(TestCase):
	"""Case of testing PostCreateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post_data = {'title': 'Some post', 'text': 'Some text'}
		self.facade = PostCreateFacade()

	def test_create(self):
		post, status_code = self.facade.create(self.post_data, self.user)

		self.assertIn('pk', post)
		self.assertEqual(post['title'], 'Some post')
		self.assertEqual(post['text'], 'Some text')
		self.assertEqual(status_code, 201)


class PostUpdateFacadeTests(TestCase):
	"""Case of testing PostUpdateFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = Post.objects.create(
			title='Some post', text='Some text'
		)
		self.post_data = {'title': 'Edited post', 'text': 'Some text'}
		self.facade = PostUpdateFacade()

	def test_update(self):
		post, status_code = self.facade.update(
			self.post.pk, self.post_data, self.user
		)

		self.assertEqual(post['title'], 'Edited post')
		self.assertEqual(post['text'], 'Some text')
		self.assertEqual(status_code, 200)


class PostDeleteFacadeTests(TestCase):
	"""Case of testing PostDeleteFacade"""

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = Post.objects.create(
			title='Some post', text='Some text'
		)
		self.facade = PostDeleteFacade()

	def test_delete(self):
		data, status_code = self.facade.delete(self.post.pk, self.user)

		self.assertIsNone(data)
		self.assertEqual(status_code, 204)
