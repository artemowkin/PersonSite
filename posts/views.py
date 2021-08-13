from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import PostGetService, PostUpdateService
from .services.facades import PostCRUDFacade


class AllCreatePostsView(BaseAllCreateView):
	"""View to render all posts entries"""

	facade_class = PostCRUDFacade


class ConcretePostView(BaseConcreteView):
	"""View to render a concrete post entry"""

	facade_class = PostCRUDFacade


class PostPreviewUploadView(BaseUploadImageView):
	"""View to upload preview image for post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
