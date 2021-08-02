from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
	"""User serializer"""

	class Meta:
		model = User
		fields = ('pk', 'username', 'email')
		read_only_fields = ('pk', 'username', 'email')
