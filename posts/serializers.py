from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
	"""Post serializer"""

	class Meta:
		model = Post
		fields = ('pk', 'title', 'text', 'preview', 'pub_date')
		read_only_fields = ('pk', 'author', 'pub_date', 'preview')
