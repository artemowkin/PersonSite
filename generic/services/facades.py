from uuid import UUID

from django.contrib.auth import get_user_model


User = get_user_model()


class BaseAPICRUDFacade:
	"""Base facade for CRUD API using services"""

	def get_concrete(self, pk: UUID) -> dict:
		"""Return a concrete entry"""
		entry = self.get_service.get_concrete(pk)
		serialized_entry = self.serializer_class(entry).data
		return (serialized_entry, 200)

	def get_all(self) -> tuple[list, int]:
		"""Return all entries"""
		all_entries = self.get_service.get_all()
		serialized_entries = self.serializer_class(all_entries, many=True).data
		return (serialized_entries, 200)

	def create(self, data: dict, user: User) -> tuple[dict, int]:
		"""Create a new entry using data"""
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			new_entry = self.create_service.create(data, user)
			serialized_entry = self.serializer_class(new_entry).data
			return (serialized_entry, 201)

		return (serializer.errors, 400)

	def update(self, pk: UUID, data: dict, user: User) -> tuple[dict, int]:
		"""Update a concrete entry"""
		serializer = self.serializer_class(data=data)
		if serializer.is_valid():
			entry = self.get_service.get_concrete(pk)
			updated_entry = self.update_service.update(entry, data, user)
			serialized_entry = self.serializer_class(updated_entry).data
			return (serialized_entry, 200)

		return (serializer.errors, 400)

	def delete(self, pk: UUID, user: User) -> tuple[type[None], int]:
		"""Delete a concrete entry"""
		entry = self.get_service.get_concrete(pk)
		self.delete_service.delete(entry, user)
		return (None, 204)
