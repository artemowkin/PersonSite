from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
	uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
	image = models.ImageField(
		'product image', upload_to='shop/products_previews'
	)
	title = models.CharField('product title', max_length=255, unique=True)
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
		return reverse('concrete_product', args=[str(self.pk)])


class ProductReview(models.Model):
	uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
	text = models.TextField('Review text')
	rating = models.PositiveIntegerField(
		'Review rating', validators=(
			MaxValueValidator(5),
		)
	)
	pub_date = models.DateField(auto_now_add=True)
	author = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='reviews',
		verbose_name='Review author'
	)
	product = models.ForeignKey(
		Product, on_delete=models.CASCADE, related_name='reviews',
		verbose_name='Reviewing product'
	)

	class Meta:
		db_table = 'product_reviews'
		ordering = ('-rating', '-pub_date')

	def __str__(self):
		return f"{self.product.title} review from {self.author.username}"

	def get_absolute_url(self):
		pass
