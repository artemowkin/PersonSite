from rest_framework.views import APIView
from rest_framework.response import Response

from .services import ProductsGetService, ProductCreateService
from .serializers import ProductSerializer


class AllCreateProductsView(APIView):
	"""View to render all products"""

	service = ProductsGetService()
	create_service = ProductCreateService()
	serializer_class = ProductSerializer

	def get(self, request):
		all_products = self.service.get_all()
		serializer = self.serializer_class(all_products, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			product = self.create_service.create(serializer.data, request.user)
			serializer_data = serializer.data
			serializer_data |= {'pk': product.pk}
			return Response(serializer_data, status=201)

		return Response(serializer.errors, status=400)


class ConcreteProductView(APIView):
	"""View to render a concrete product"""

	get_service = ProductsGetService()
	serializer_class = ProductSerializer

	def get(self, request, pk):
		concrete_product = self.get_service.get_concrete(pk)
		serializer = self.serializer_class(concrete_product)
		return Response(serializer.data)
