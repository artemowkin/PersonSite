from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseCommandView(APIView):
	"""Base view with using commands"""

	def get_command_response(self, command):
		data, status_code = command.execute()
		return Response(data, status=status_code)


class BaseAllCreateView(BaseCommandView):
	"""Base view to render all entries and create a new entry"""

	create_command_class = None
	get_command_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.create_command_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`create_command_class` attribute"
			)
		if not self.get_command_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_command` attribute"
			)

	def get(self, request, *args, **kwargs):
		get_command = self.get_command_class(*args, **kwargs)
		return self.get_command_response(get_command)

	def post(self, request, *args, **kwargs):
		create_command = self.create_command_class(
			request.data, request.user, *args, **kwargs
		)
		return self.get_command_response(create_command)


class BaseConcreteView(BaseCommandView):
	"""Base view to render a concrete entry, update it, and delete it"""

	get_command_class = None
	update_command_class = None
	delete_command_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.get_command_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_command_class` attribute"
			)
		if not self.update_command_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`update_command_class` attribute"
			)
		if not self.delete_command_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`delete_command_class` attribute"
			)

	def get(self, request, pk):
		get_command = self.get_command_class(pk)
		return self.get_command_response(get_command)

	def put(self, request, pk):
		update_command = self.update_command_class(
			pk, request.data, request.user
		)
		return self.get_command_response(update_command)

	def delete(self, request, pk):
		delete_command = self.delete_command_class(pk, request.user)
		return self.get_command_response(delete_command)


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
