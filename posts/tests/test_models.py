from datetime import date
from uuid import UUID

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post


User = get_user_model()


class PostModelTests(TestCase):
	"""Case of testing Post model"""

	model = Post

	def setUp(self):
		self.user = User.objects.create_superuser(
			username='testuser', password='testpass'
		)
		self.post = self.model.objects.create(
			title='Some post', text='Some text'
		)

	def test_model_entry_fields(self):
		"""Test are created model entry's fields valid"""
		self.assertIsInstance(self.post.pk, UUID)
		self.assertEqual(self.post.title, 'Some post')
		self.assertEqual(self.post.text, 'Some text')
		self.assertEqual(self.post.pub_date, date.today())

	def test_string_representation(self):
		"""Test is created model entry's string representation valid"""
		string_entry = str(self.post)

		self.assertEqual(string_entry, self.post.title)

	def test_absolute_url(self):
		"""Test does get_absolute_url() method return a valid url"""
		url = self.post.get_absolute_url()

		self.assertEqual(url, f'/posts/{self.post.pk}/')
