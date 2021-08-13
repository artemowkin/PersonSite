from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import PostGetService, PostUpdateService
from .services.commands import (
	GetAllPostsCommand, CreatePostCommand, GetConcretePostCommand,
	UpdatePostCommand, DeletePostCommand
)


class AllCreatePostsView(BaseAllCreateView):
	"""View to render all posts entries"""

	get_command_class = GetAllPostsCommand
	create_command_class = CreatePostCommand


class ConcretePostView(BaseConcreteView):
	"""View to render a concrete post entry"""

	get_command_class = GetConcretePostCommand
	update_command_class = UpdatePostCommand
	delete_command_class = DeletePostCommand


class PostPreviewUploadView(BaseUploadImageView):
	"""View to upload preview image for post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
