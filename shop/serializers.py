from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
	"""Product serializer"""

	class Meta:
		model = Product
		fields = (
			'pk', 'image', 'title', 'short_description', 'description',
			'price', 'amount', 'available'
		)
		read_only_fields = ('pk', 'image')
