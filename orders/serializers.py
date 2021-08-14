from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
	"""Order serializer"""

	customer = UserSerializer(required=False)

	class Meta:
		model = Order
		fields = (
			'pk', 'first_name', 'last_name', 'address', 'postal_code',
			'city', 'status', 'customer', 'pub_date'
		)
		read_only_fields = ('pk', 'customer', 'pub_date')
