from generic.services.commands import BaseGetAllCommand

from .base import PostGetService
from ..serializers import PostSerializer


class GetAllPostsCommand(BaseGetAllCommand):
	"""Command to get all posts"""

	get_service_class = PostGetService
	serializer_class = PostSerializer
