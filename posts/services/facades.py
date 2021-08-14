from generic.services.facades import (
	BaseGetFacade, BaseCreateFacade, BaseUpdateFacade, BaseDeleteFacade
)
from .base import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from ..serializers import PostSerializer


class PostGetFacade(BaseGetFacade):
	"""Facade to get posts using services"""

	serializer_class = PostSerializer

	def __init__(self):
		self.get_service = PostGetService()


class PostCreateFacade(BaseCreateFacade):
	"""Facade to create a new post using services"""

	serializer_class = PostSerializer

	def __init__(self):
		self.create_service = PostCreateService()


class PostUpdateFacade(BaseUpdateFacade):
	"""Facade to update a concrete post using services"""

	serializer_class = PostSerializer

	def __init__(self):
		self.get_service = PostGetService()
		self.update_service = PostUpdateService()


class PostDeleteFacade(BaseDeleteFacade):
	"""Facade to delete a concrete post using services"""

	serializer_class = PostSerializer

	def __init__(self):
		self.get_service = PostGetService
		self.delete_service = PostDeleteService
