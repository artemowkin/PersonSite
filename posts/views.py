from rest_framework.views import APIView
from rest_framework.response import Response

from generic.views import BaseAllCreateView
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


class ConcretePostView(APIView):
	"""View to render a concrete post entry"""

	get_service = PostGetService()
	update_service = PostUpdateService()
	delete_service = PostDeleteService()
	serializer_class = PostSerializer

	def get(self, request, pk):
		concrete_post = self.get_service.get_concrete(pk)
		serializer = self.serializer_class(concrete_post)
		return Response(serializer.data)

	def put(self, request, pk):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			concrete_post = self.get_service.get_concrete(pk)
			changed_post = self.update_service.update(
				concrete_post, request.data, request.user
			)
			serialized_post = self.serializer_class(changed_post)
			return Response(serialized_post.data, status=200)

		return Response(serializer.errors, status=400)

	def delete(self, request, pk):
		concrete_post = self.get_service.get_concrete(pk)
		self.delete_service.delete(concrete_post, request.user)
		return Response(status=204)
