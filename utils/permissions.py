from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
	"""Permission check is user in request an admin"""

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		return request.user.is_superuser
