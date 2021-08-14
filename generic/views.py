from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseAllCreateView(APIView):
	"""Base view to render all entries and create a new entry"""

	get_facade_class = None
	create_facade_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_facade_class` attribute"
			)
		if not self.create_facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`create_facade_class` attribute"
			)

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.setup_facades()

	def setup_facades(self):
		self.get_facade = self.get_facade_class()
		self.create_facade = self.create_facade_class()

	def get(self, request):
		data, status_code = self.get_facade.get_all()
		return Response(data, status=status_code)

	def post(self, request):
		data, status_code = self.create_facade.create(
			request.data, request.user
		)
		return Response(data, status=status_code)


class BaseConcreteView(APIView):
	"""Base view to render a concrete entry, update it, and delete it"""

	get_facade_class = None
	update_facade_class = None
	delete_facade_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_facade_class` attribute"
			)
		if not self.update_facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`update_facade_class` attribute"
			)
		if not self.delete_facade_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`delete_facade_class` attribute"
			)

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.setup_facades()

	def setup_facades(self):
		self.get_facade = self.get_facade_class()
		self.update_facade = self.update_facade_class()
		self.delete_facade = self.delete_facade_class()

	def get(self, request, pk):
		data, status_code = self.get_facade.get_concrete(pk)
		return Response(data, status=status_code)

	def put(self, request, pk):
		data, status_code = self.update_facade.update(
			pk, request.data, request.user
		)
		return Response(data, status=status_code)

	def delete(self, request, pk):
		data, status_code = self.delete_facade.delete(pk, request.user)
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
