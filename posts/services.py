from typing import TextIO

from django.db.models import QuerySet

from generic.services import (
	BaseGetService, BaseModelService, BaseCreateService,
	BaseUpdateService, BaseDeleteService
)
from generic.strategies import CheckIsUserAdminStrategy

from .models import Post


class PostGetService(BaseGetService):
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

	def update_image(self, post: Post, file_obj: TextIO) -> None:
		post.preview = file_obj
		post.save()


class PostDeleteService(BaseDeleteService):
	"""Service to delete a concrete post entry"""

	check_user_strategy = CheckIsUserAdminStrategy()
