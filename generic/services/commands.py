from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer


User = get_user_model()


class BaseGetCommand:
	"""Base command to get all/concrete entries"""

	get_service_class = None
	serializer_class = None

	def check_attributes(self):
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


class BaseGetAllCommand(BaseGetCommand):
	"""Base command to get all entries"""

	def __init__(self):
		self.check_attributes()
		self._get_service = self.get_service_class()

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
		self.check_attributes()
		self._data = data
		self._user = user
		self._create_service = self.create_service_class()

	def check_attributes(self):
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
			return (serialized_entry, 201)

		return (serializer.errors, 400)

	def _create_entry(self, serializer: Serializer) -> dict:
		"""Create a new entry and return this serialized entry"""
		entry = self._create_service.create(serializer.data, self._user)
		serialized_entry = self.serializer_class(entry).data
		return serialized_entry


class BaseGetConcreteCommand(BaseGetCommand):
	"""Base command to get a concrete entry"""

	def __init__(self, pk: UUID):
		self.check_attributes()
		self._pk = pk
		self._get_service = self.get_service_class()

	def execute(self) -> tuple[dict, int]:
		"""
		Get a concrete entry and return this serialized entry
		and status code of response
		"""
		concrete_entry = self._get_service.get_concrete(self._pk)
		serializer = self.serializer_class(concrete_entry)
		return (serializer.data, 200)


class UpdateEntryMixin:
	"""Mixin to update a concrete entry"""

	def change_entry(self, entry: Model, serializer: Serializer) -> dict:
		"""Change the entry and return this changed serilaized entry"""
		changed_entry = self._update_service.update(
			entry, serializer.data, self._user
		)
		serialized_entry = self.serializer_class(changed_entry)
		return serialized_entry.data


class BaseUpdateCommand(BaseGetCommand, UpdateEntryMixin):
	"""Base command to update a concrete entry"""

	update_service_class = None
	serializer_class = None

	def __init__(self, pk: UUID, data: dict, user: User):
		self.check_attributes()
		self._pk = pk
		self._data = data
		self._user = user
		self._get_service = self.get_service_class()
		self._update_service = self.update_service_class()

	def check_attributes(self):
		super().check_attributes()
		if not self.update_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`update_service_class` attribute"
			)

	def execute(self) -> tuple[dict, int]:
		"""
		Update a concrete entry and return this serialized entry
		(or error messages) and response status code
		"""
		serializer = self.serializer_class(data=self._data)
		if serializer.is_valid():
			concrete_entry = self._get_service.get_concrete(self._pk)
			changed_entry = self.change_entry(concrete_entry, serializer)
			return (changed_entry, 200)

		return Response(serializer.errors, status=400)


class BaseDeleteCommand(BaseGetCommand):
	"""Base command to delete a concrete entry"""

	delete_service_class = None
	serializer_class = None

	def __init__(self, pk: UUID, user: User):
		self.check_attributes()
		self._pk = pk
		self._user = user
		self._get_service = self.get_service_class()
		self._delete_service = self.delete_service_class()

	def check_attributes(self):
		super().check_attributes()
		if not self.delete_service_class:
			raise ImproperlyConfigured(
				f"{self.__class__.__name__} must have "
				"`delete_service_class` attribute"
			)

	def execute(self) -> tuple[None, int]:
		"""Delete a concrete entry and return 204 response"""
		concrete_entry = self._get_service.get_concrete(self._pk)
		self._delete_service.delete(concrete_entry, self._user)
		return (None, 204)
