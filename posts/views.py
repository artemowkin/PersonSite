from rest_framework.views import APIView
from rest_framework.response import Response

from generic.views import BaseAllCreateView, BaseConcreteView
from .services import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from .serializers import PostSerializer


class AllCreatePostsView(BaseAllCreateView):
	"""View to render all posts entries"""

	create_service = PostCreateService()
	get_service = PostGetService()
	serializer_class = PostSerializer


class PostPreviewUploadView(APIView):
	"""View to upload preview image for post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()

	def put(self, request, pk):
		file_obj = request.data.get('file')
		if not file_obj:
			return Response(
				{"error": "You need to send the file"}, status=400
			)

		post = self.get_service.get_concrete(pk)
		self.update_service.update_preview(post, file_obj)
		return Response(status=204)


class ConcretePostView(BaseConcreteView):
	"""View to render a concrete post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
	delete_service = PostDeleteService()
	serializer_class = PostSerializer
