from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
	STATUS_CHOICES = (
		('processing', 'processing'),
		('viewed', 'viewed'),
		('sent', 'sent'),
		('arrived', 'arrived'),
	)
	uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
	first_name = models.CharField('customer first name', max_length=50)
	last_name = models.CharField('customer last name', max_length=50)
	address = models.CharField('customer address', max_length=255)
	postal_code = models.CharField('customer postal code', max_length=20)
	city = models.CharField('customer city', max_length=100)
	status = models.CharField(
		'order status', max_length=15, default='processing',
		choices=STATUS_CHOICES
	)
	customer = models.ForeignKey(
		User, on_delete=models.CASCADE, related_name='orders',
		verbose_name='Customer user'
	)
	pub_date = models.DateField(auto_now_add=True)

	class Meta:
		db_table = 'orders'
		ordering = ('-pub_date', 'status')

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.city})"

	def get_absolute_url(self):
		pass
