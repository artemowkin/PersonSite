from django.urls import path

from . import views


urlpatterns = [
	path('', views.AllCreateProductsView.as_view(), name='all_products'),
]
