from rest_framework.views import APIView
from rest_framework.response import Response

from generic.views import BaseAllCreateView
from .services import (
	ProductsGetService, ProductCreateService, ProductUpdateService
)
from .serializers import ProductSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	create_service = ProductCreateService()
	get_service = ProductsGetService()
	serializer_class = ProductSerializer


class ConcreteProductView(APIView):
	"""View to render a concrete product"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()
	serializer_class = ProductSerializer

	def get(self, request, pk):
		concrete_product = self.get_service.get_concrete(pk)
		serializer = self.serializer_class(concrete_product)
		return Response(serializer.data)

	def put(self, request, pk):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			concrete_product = self.get_service.get_concrete(pk)
			changed_product = self.update_service.update(
				concrete_product, request.data, request.user
			)
			serialized_product = self.serializer_class(changed_product)
			return Response(serialized_product.data, status=200)

		return Response(serializer.errors, status=400)
