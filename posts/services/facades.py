from generic.services.facades import BaseAPICRUDFacade
from .base import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from ..serializers import PostSerializer


class PostCRUDFacade(BaseAPICRUDFacade):
	"""Facade with CRUD functionality using services"""
	serializer_class = PostSerializer

	def __init__(self):
		self.get_service = PostGetService()
		self.create_service = PostCreateService()
		self.update_service = PostUpdateService()
		self.delete_service = PostDeleteService()