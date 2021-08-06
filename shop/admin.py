from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
		'title', 'short_description', 'price', 'amount', 'available'
	)
	list_filter = ('available',)
	search_fields = ('title', 'short_description')
