from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post


User = get_user_model()


class BaseViewTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.client.login(username='testuser', password='testpass')


class AllCreatePostsViewTests(BaseViewTest):
	"""Case of testing AllCreatePostsView view"""

	urlpattern = 'all_posts'

	def test_get(self):
		"""Test does GET request return 200 response"""
		response = self.client.get(reverse(self.urlpattern))
		self.assertEqual(response.status_code, 200)

	def test_post(self):
		"""Test does POST request return 201 response"""
		response = self.client.post(reverse(self.urlpattern), {
			'title': 'Some post', 'text': 'Some text'
		}, content_type='application/json')
		self.assertEqual(response.status_code, 201)


class ConcretePostViewTests(BaseViewTest):
	"""Case of testing ConcretePostView view"""

	model = Post
	urlpattern = 'concrete_post'

	def setUp(self):
		super().setUp()
		self.post = self.model.objects.create(
			title='Some post', text='Some text', author=self.user
		)

	def test_get(self):
		"""Test does GET request return 200 response"""
		response = self.client.get(reverse(
			self.urlpattern, args=(str(self.post.pk),)
		))
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		"""Test does PUT request return 201 response"""
		response = self.client.put(
			reverse(self.urlpattern, args=(str(self.post.pk),)),
			{'title': 'Edited post', 'text': 'Some text'},
			content_type='application/json'
		)
		self.assertEqual(response.status_code, 200)

	def test_delete(self):
		"""Test does DELETE request return 200 response"""
		response = self.client.delete(reverse(
			self.urlpattern, args=(str(self.post.pk),)
		))
		self.assertEqual(response.status_code, 204)


class UserPostsViewTests(BaseViewTest):
	"""Case of testing UserPostsView view"""

	urlpattern = 'user_posts'

	def test_get(self):
		"""Test does GET request return 200 response"""
		response = self.client.get(
			reverse(self.urlpattern, args=(self.user.pk,))
		)
		self.assertEqual(response.status_code, 200)
