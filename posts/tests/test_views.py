from django.urls import reverse
from django.test import TestCase

from generic.unit_tests import AllCreateViewMixin, ConcreteViewMixin
from ..models import Post


class AllCreatePostsViewTests(AllCreateViewMixin, TestCase):
	"""Case of testing AllCreatePostsView view"""

	urlpattern = 'all_posts'

	def setUp(self):
		super().setUp()
		self.post_request_data = {'title': 'Some post', 'text': 'Some text'}


class ConcretePostViewTests(ConcreteViewMixin, TestCase):
	"""Case of testing ConcretePostView view"""

	model = Post
	urlpattern = 'concrete_post'

	def setUp(self):
		super().setUp()
		self.entry = self.model.objects.create(
			title='Some post', text='Some text'
		)
		self.put_request_data = {'title': 'Edited post', 'text': 'Some text'}
