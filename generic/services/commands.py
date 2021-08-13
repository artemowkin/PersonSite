from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer


User = get_user_model()


class BaseGetAllCommand:
	"""Base command to get all entries"""

	get_service_class = None
	serializer_class = None

	def __init__(self):
		self._check_attributes()
		self._get_service = self.get_service_class()

	def _check_attributes(self):
		if not self.get_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`get_service_class` attribute"
			)
		if not self.serializer_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`serializer_class` attribute"
			)

	def execute(self) -> tuple[dict, int]:
		"""
		Get all entries and return serialized list with these
		entries, and status code of response
		"""
		all_entries = self._get_service.get_all()
		serializer = self.serializer_class(all_entries, many=True)
		return (serializer.data, 200)


class BaseCreateCommand:
	"""Base command to create a new entry"""

	create_service_class = None
	serializer_class = None

	def __init__(self, data: dict, user: User):
		self._check_attributes()
		self._data = data
		self._user = user
		self._create_service = self.create_service_class()

	def _check_attributes(self):
		if not self.create_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`create_service_class` attribute"
			)
		if not self.serializer_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`serializer_class` attribute"
			)

	def execute(self) -> tuple[dict, int]:
		"""
		Create a new entry and return this serialized entry
		(or error messages) and response status code
		"""
		serializer = self.serializer_class(data=self._data)
		if serializer.is_valid():
			serialized_entry = self._create_entry(serializer)
			return (serializer_entry, 201)

		return (serializer.errors, 400)

	def _create_entry(self, serializer: Serializer) -> dict:
		"""Create a new entry and return this serialized entry"""
		entry = self._create_service.create(serializer.data, self._user)
		serialized_entry = self.serializer_class(entry).data
		return serialized_entry