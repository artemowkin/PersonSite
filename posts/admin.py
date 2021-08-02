from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'pub_date']
	date_hierarchy = 'pub_date'
	raw_id_fields = ['author']
	search_fields = ['title', 'author']
