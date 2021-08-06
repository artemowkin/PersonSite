from uuid import uuid4

from django.db import models


class Product(models.Model):
	uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
	image = models.ImageField(
		'product image', upload_to='shop/products_previews'
	)
	title = models.CharField('product title', max_length=255)
	short_description = models.CharField(
		'product short description', max_length=255
	)
	description = models.TextField('product description')
	price = models.DecimalField(
		'product price', max_digits=10, decimal_places=2
	)
	amount = models.PositiveIntegerField('product amount')
	available = models.BooleanField('is product available', default=True)

	class Meta:
		db_table = 'products'
		ordering = ('available', '-amount', '-price')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		pass
