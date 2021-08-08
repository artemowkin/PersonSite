from rest_framework.views import APIView
from rest_framework.response import Response

from generic.views import BaseAllCreateView, BaseConcreteView
from .services import (
	ProductsGetService, ProductCreateService, ProductUpdateService,
	ProductDeleteService
)
from .serializers import ProductSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	create_service = ProductCreateService()
	get_service = ProductsGetService()
	serializer_class = ProductSerializer


class ConcreteProductView(BaseConcreteView):
	"""View to render a concrete product"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()
	delete_service = ProductDeleteService()
	serializer_class = ProductSerializer
