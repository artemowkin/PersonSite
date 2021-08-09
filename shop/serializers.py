from rest_framework import serializers

from .models import Product, ProductReview


class ProductSerializer(serializers.ModelSerializer):
	"""Product serializer"""

	class Meta:
		model = Product
		fields = (
			'pk', 'image', 'title', 'short_description', 'description',
			'price', 'amount', 'available'
		)
		read_only_fields = ('pk', 'image')


class ProductReviewSerializer(serializers.ModelSerializer):
	"""ProductReview serializer"""

	class Meta:
		model = ProductReview
		fields = ('pk', 'text', 'rating', 'pub_date', 'author', 'product')
		read_only_fields = ('pk', 'pub_date', 'author', 'product')
