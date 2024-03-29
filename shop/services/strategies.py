from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Model

from generic.services.strategies import BaseCheckUserStrategy


User = get_user_model()


class CheckIsUserAdminOrAuthorStrategy(BaseCheckUserStrategy):
	"""Strategy to check is user admin or an author of review"""

	def check_entry_user(self, user: User, entry: Model):
		if not user.is_superuser and entry.author != user:
			raise PermissionDenied
