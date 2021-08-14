from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import PostGetService, PostUpdateService
from .services.facades import (
	PostGetFacade, PostCreateFacade, PostUpdateFacade, PostDeleteFacade
)


class AllCreatePostsView(BaseAllCreateView):
	"""View to render all posts entries"""

	get_facade_class = PostGetFacade
	create_facade_class = PostCreateFacade


class ConcretePostView(BaseConcreteView):
	"""View to render a concrete post entry"""

	get_facade_class = PostGetFacade
	update_facade_class = PostUpdateFacade
	delete_facade_class = PostDeleteFacade


class PostPreviewUploadView(BaseUploadImageView):
	"""View to upload preview image for post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
