from django.urls import reverse

from generic.module_tests import BaseViewTest
from ..models import Post


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
			title='Some post', text='Some text'
		)

	def test_get(self):
		"""Test does GET request return 200 response"""
		response = self.client.get(reverse(
			self.urlpattern, args=(str(self.post.pk),)
		))
		self.assertEqual(response.status_code, 200)

	def test_put(self):
		"""Test does PUT request return 200 response"""
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
