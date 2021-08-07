from typing import TextIO

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet

from generic.services import (
	BaseGetEntryService, BaseModelService, check_is_user_superuser,
	BaseCreateService, BaseUpdateService
)
from generic.strategies import CheckIsUserAdminStrategy

from .models import Post


User = get_user_model()


class PostGetService(BaseGetEntryService):
	"""Service to get posts entries"""

	model = Post

	def get_user_posts(self, user_pk: int) -> QuerySet:
		"""Return concrete user posts"""
		return self.model.objects.filter(author__pk=user_pk)


class PostCreateService(BaseCreateService):
	"""Service to create a new post entry"""

	model = Post
	check_user_strategy = CheckIsUserAdminStrategy()


class PostUpdateService(BaseUpdateService):
	"""Service to update a concrete post entry"""

	check_user_strategy = CheckIsUserAdminStrategy()

	def set_entry_fields(self, entry: Post, data: dict) -> None:
		entry.title = data['title']
		entry.text = data['text']

	def update_preview(self, post: Post, file_obj: TextIO) -> None:
		post.preview = file_obj
		post.save()


class PostDeleteService:
	"""Service to delete a concrete post entry"""

	def delete(self, post: Post, user: User) -> None:
		check_is_user_superuser(user)
		post.delete()
