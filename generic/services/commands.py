from uuid import UUID

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer


User = get_user_model()


class BaseGetAllCommand:
	"""Base command to get all entries"""

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

	def execute(self) -> tuple[dict, int]:
		"""
		Create a new entry and return this serialized entry
		(or error messages) and response status code
		"""
		serializer = self.serializer_class(data=self._data)
		if serializer.is_valid():
			serialized_entry = self.create_entry(serializer)
			return (serialized_entry, 201)

		return (serializer.errors, 400)

	def create_entry(self, serializer: Serializer) -> dict:
		"""Create a new entry and return this serialized entry"""
		entry = self._create_service.create(serializer.data, self._user)
		serialized_entry = self.serializer_class(entry).data
		return serialized_entry


class ConcreteEntryMixin:
	"""Mixin with logic to get a concrete entry"""

	def get_concrete_entry(self) -> dict:
		return self._get_service.get_concrete(self._pk)


class BaseGetConcreteCommand(ConcreteEntryMixin):
	"""Base command to get a concrete entry"""

	def execute(self) -> tuple[dict, int]:
		"""
		Get a concrete entry and return this serialized entry
		and status code of response
		"""
		concrete_entry = self.get_concrete_entry()
		serializer = self.serializer_class(concrete_entry)
		return (serializer.data, 200)


class BaseUpdateCommand(ConcreteEntryMixin):
	"""Base command to update a concrete entry"""

	def execute(self) -> tuple[dict, int]:
		"""
		Update a concrete entry and return this serialized entry
		(or error messages) and response status code
		"""
		serializer = self.serializer_class(data=self._data)
		if serializer.is_valid():
			concrete_entry = self.get_concrete_entry()
			concrete_entry = self._get_service.get_concrete(self._pk)
			changed_entry = self.change_entry(concrete_entry, serializer)
			return (changed_entry, 200)

		return Response(serializer.errors, status=400)

	def change_entry(self, entry: Model, serializer: Serializer) -> dict:
		"""Change the entry and return this changed serilaized entry"""
		changed_entry = self._update_service.update(
			entry, serializer.data, self._user
		)
		serialized_entry = self.serializer_class(changed_entry)
		return serialized_entry.data


class BaseDeleteCommand(ConcreteEntryMixin):
	"""Base command to delete a concrete entry"""

	def execute(self) -> tuple[None, int]:
		"""Delete a concrete entry and return 204 response"""
		concrete_entry = self.get_concrete_entry()
		self._delete_service.delete(concrete_entry, self._user)
		return (None, 204)
