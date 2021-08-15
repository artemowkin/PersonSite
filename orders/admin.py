from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		'first_name', 'last_name', 'city', 'address', 'postal_code', 'status',
		'pub_date'
	)
	list_filter = ('status',)
	search_fields = ('first_name', 'last_name', 'city', 'address')
	raw_id_fields = ('customer',)
