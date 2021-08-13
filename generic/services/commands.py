from django.core.exceptions import ImproperlyConfigured


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
