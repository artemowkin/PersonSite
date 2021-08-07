from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response


class BaseAllCreateView(APIView):
	"""Base view to render all entries and create a new entry"""

	create_service = None
	get_service = None
	serializer_class = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.create_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`create_service` attribute"
			)
		if not self.get_service:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_service` attribute"
			)
		if not self.serializer_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`serializer_class` attribute"
			)

	def get(self, request):
		all_entries = self.get_service.get_all()
		serializer = self.serializer_class(all_entries, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			entry = self.create_service.create(serializer.data, request.user)
			serializer_data = serializer.data
			serializer_data |= {'pk': entry.pk}
			return Response(serializer_data, status=201)

		return Response(serializer.errors, status=400)
