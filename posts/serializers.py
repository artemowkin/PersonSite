from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
	"""Post serializer"""

	author = UserSerializer(read_only=True)

	class Meta:
		model = Post
		fields = ['pk', 'title', 'text', 'preview', 'author', 'pub_date']
		read_only_fields = ['pk', 'author', 'pub_date', 'preview']
