from django.test import TestCase
from django.contrib.auth import get_user_model
from django.http import Http404
from django.core.exceptions import PermissionDenied

from generic.unit_tests import (
	GetServiceMixin, CreateServiceMixin, UpdateServiceMixin,
	DeleteServiceMixin
)
from ..models import Post
from ..services import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)


User = get_user_model()


class PostGetServiceTests(GetServiceMixin, TestCase):
	"""Case of testing PostGetService service"""

	model = Post
	service = PostGetService()

	def setUp(self):
		self.entry = self.model.objects.create(
			title='Some post', text='Some text'
		)


class PostCreateServiceTests(CreateServiceMixin, TestCase):
	"""Case of testing PostCreateService service"""

	model = Post
	service = PostCreateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry_data = {'title': 'Some post', 'text': 'Some text'}

	def check_created_entry_fields(self, entry):
		self.assertEqual(entry.title, 'Some post')
		self.assertEqual(entry.text, 'Some text')


class PostUpdateServiceTests(UpdateServiceMixin, TestCase):
	"""Case of testing PostUpdateService service"""

	model = Post
	service = PostUpdateService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = self.model.objects.create(
			title='Some post', text='Some text'
		)
		self.entry_data = {'title': 'Edited post', 'text': 'Some text'}

	def check_updated_entry_fields(self, entry):
		self.assertEqual(entry.title, 'Edited post')
		self.assertEqual(entry.text, 'Some text')


class PostDeleteServiceTests(DeleteServiceMixin, TestCase):
	"""Case of testing PostDeleteService service"""

	model = Post
	service = PostDeleteService()

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.entry = self.model.objects.create(
			title='Some post', text='Some text'
		)
