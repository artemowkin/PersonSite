from django.urls import path

from . import views


urlpatterns = [
	path('', views.AllCreateProductsView.as_view(), name='all_products'),
	path(
		'<uuid:pk>/', views.ConcreteProductView.as_view(),
		name='concrete_product'
	),
	path(
		'<uuid:pk>/set_image/', views.ProductImageUploadView.as_view(),
		name='product_image_view'
	),
	path(
		'<uuid:pk>/reviews/', views.AllProductReviewsView.as_view(),
		name='all_product_reviews'
	),
	path(
		'<uuid:product_pk>/reviews/<uuid:review_pk>/',
		views.ConcreteProductReviewView.as_view(),
		name='concrete_product_review'
	),
]
