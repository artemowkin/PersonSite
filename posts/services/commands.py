from generic.services.commands import (
	BaseGetAllCommand, BaseCreateCommand, BaseGetConcreteCommand,
	BaseUpdateCommand, BaseDeleteCommand
)

from .base import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from ..serializers import PostSerializer


class GetAllPostsCommand(BaseGetAllCommand):
	"""Command to get all posts"""

	get_service_class = PostGetService
	serializer_class = PostSerializer


class GetConcretePostCommand(BaseGetConcreteCommand):
	"""Command to get a concrete post"""

	get_service_class = PostGetService
	serializer_class = PostSerializer


class CreatePostCommand(BaseCreateCommand):
	"""Command to create a new post"""

	create_service_class = PostCreateService
	serializer_class = PostSerializer


class UpdatePostCommand(BaseUpdateCommand):
	"""Command to update a concrete post"""

	get_service_class = PostGetService
	update_service_class = PostUpdateService
	serializer_class = PostSerializer


class DeletePostCommand(BaseDeleteCommand):
	"""Command to delete a concrete post"""

	get_service_class = PostGetService
	delete_service_class = PostDeleteService
	serializer_class = PostSerializer
