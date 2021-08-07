from typing import TextIO

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet

from generic.services import (
	BaseGetEntryService, BaseModelService, check_is_user_superuser,
	BaseAdminCreateService
)

from .models import Post


User = get_user_model()


class PostGetService(BaseGetEntryService):
	"""Service to get posts entries"""

	model = Post

	def get_user_posts(self, user_pk: int) -> QuerySet:
		"""Return concrete user posts"""
		return self.model.objects.filter(author__pk=user_pk)


class PostCreateService(BaseAdminCreateService):
	"""Service to create a new post entry"""

	model = Post


class PostUpdateService:
	"""Service to update a concrete post entry"""

	def update(self, post: Post, data: dict, user: User) -> Post:
		check_is_user_superuser(user)
		post.title = data['title']
		post.text = data['text']
		post.save()
		return post

	def update_preview(self, post: Post, file_obj: TextIO) -> None:
		post.preview = file_obj
		post.save()


class PostDeleteService:
	"""Service to delete a concrete post entry"""

	def delete(self, post: Post, user: User) -> None:
		check_is_user_superuser(user)
		post.delete()
