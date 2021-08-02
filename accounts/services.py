from django.contrib.auth import get_user_model

from generic.services import BaseGetEntryService


User = get_user_model()


class UserGetService(BaseGetEntryService):
	"""Service to get users"""

	model = User
