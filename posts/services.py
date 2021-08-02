from typing import TextIO

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet

from generic.services import BaseGetEntryService, BaseModelService

from .models import Post


User = get_user_model()


def _validate_post_author(post: Post, user: User) -> None:
	"""Validate does the post author equals user"""
	if not post.author == user:
		raise PermissionDenied


class PostGetService(BaseGetEntryService):
	"""Service to get posts entries"""

	model = Post

	def get_user_posts(self, user_pk: int) -> QuerySet:
		"""Return concrete user posts"""
		return self.model.objects.filter(author__pk=user_pk)


class PostCreateService(BaseModelService):
	"""Service to create a new post entry"""

	model = Post

	def create(self, data: dict, user: User) -> Post:
		return self.model.objects.create(**data, author=user)


class PostUpdateService:
	"""Service to update a concrete post entry"""

	def update(self, post: Post, data: dict, user: User) -> Post:
		_validate_post_author(post, user)
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
		_validate_post_author(post, user)
		post.delete()
