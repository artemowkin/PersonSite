from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from .services.commands import GetAllPostsCommand
from .serializers import PostSerializer


class AllCreatePostsView(BaseAllCreateView):
	"""View to render all posts entries"""

	create_service = PostCreateService()
	get_command_class = GetAllPostsCommand
	serializer_class = PostSerializer


class ConcretePostView(BaseConcreteView):
	"""View to render a concrete post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
	delete_service = PostDeleteService()
	serializer_class = PostSerializer


class PostPreviewUploadView(BaseUploadImageView):
	"""View to upload preview image for post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
