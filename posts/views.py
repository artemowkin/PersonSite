from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.services import UserGetService
from .services import (
	PostGetService, PostCreateService, PostUpdateService, PostDeleteService
)
from .serializers import PostSerializer


class AllCreatePostsView(APIView):
	"""View to render all posts entries"""

	create_service = PostCreateService()
	service = PostGetService()
	serializer_class = PostSerializer

	def get(self, request):
		all_posts = self.service.get_all()
		serializer = self.serializer_class(all_posts, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			post = self.create_service.create(serializer.data, request.user)
			serializer_data = serializer.data
			serializer_data |= {'pk': post.pk}
			return Response(serializer_data, status=201)

		return Response(serializer.errors)


class PostPreviewUploadView(APIView):
	"""View to upload preview image for post entry"""

	service = PostGetService()

	def put(self, request, pk, filename):
		file_obj = request.data.get('file')
		if not file_obj:
			return Response(
				{"error": "You need to send the file"}, status=400
			)

		post = self.service.get_concrete(pk)
		post.preview = file_obj
		post.save()
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
		concrete_post = self.get_service.get_concrete(pk)
		changed_post = self.update_service.update(
			concrete_post, request.data, request.user
		)
		serialized_post = self.serializer_class(changed_post)
		return Response(serialized_post.data, status=204)

	def delete(self, request, pk):
		concrete_post = self.get_service.get_concrete(pk)
		self.delete_service.delete(concrete_post, request.user)
		return Response(status=204)


class UserPostsView(APIView):
	"""View to render all user posts entries"""

	user_service = UserGetService()
	post_service = PostGetService()
	serializer_class = PostSerializer

	def get(self, request, user_pk):
		user = self.user_service.get_concrete(user_pk)
		user_posts = self.post_service.get_user_posts(user)
		serializer = self.serializer_class(user_posts, many=True)
		return Response(serializer.data)
