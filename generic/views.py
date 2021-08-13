from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseFacadeView(APIView):
	"""Base view using facade"""

	facade_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`facade_class` attribute"
			)

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.facade = self.create_facade()

	def create_facade(self):
		return self.facade_class()


class BaseAllCreateView(BaseFacadeView):
	"""Base view to render all entries and create a new entry"""

	def get(self, request):
		data, status_code = self.facade.get_all()
		return Response(data, status=status_code)

	def post(self, request):
		data, status_code = self.facade.create(request.data, request.user)
		return Response(data, status=status_code)


class BaseConcreteView(BaseFacadeView):
	"""Base view to render a concrete entry, update it, and delete it"""

	def get(self, request, pk):
		data, status_code = self.facade.get_concrete(pk)
		return Response(data, status=status_code)

	def put(self, request, pk):
		data, status_code = self.facade.update(pk, request.data, request.user)
		return Response(data, status=status_code)

	def delete(self, request, pk):
		data, status_code = self.facade.delete(pk, request.user)
		return Response(data, status=status_code)


class BaseUploadImageView(APIView):
	"""Base view to upload images for entries"""

	get_service = None
	update_service = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_service` attribute"
			)
		if not self.update_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`update_service` attribute"
			)

	def put(self, request, pk):
		file_obj = request.data.get('file')
		if not file_obj:
			return Response(
				{"error": "You need to send the file"}, status=400
			)

		entry = self.get_service.get_concrete(pk)
		self.update_service.update_image(entry, file_obj)
		return Response(status=204)
