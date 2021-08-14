from django.urls import path

from . import views


urlpatterns = [
	path('', views.AllCreateOrdersView.as_view(), name='all_orders'),
]
