from generic.services.commands import BaseGetAllCommand, BaseCreateCommand

from .base import PostGetService, PostCreateService
from ..serializers import PostSerializer


class GetAllPostsCommand(BaseGetAllCommand):
	"""Command to get all posts"""

	get_service_class = PostGetService
	serializer_class = PostSerializer


class CreatePostCommand(BaseCreateCommand):
	"""Command to create a new post"""

	create_service_class = PostCreateService
	serializer_class = PostSerializer
