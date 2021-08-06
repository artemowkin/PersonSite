from rest_framework.views import APIView
from rest_framework.response import Response

from .services import ProductsGetService
from .serializers import ProductSerializer


class AllCreateProductsView(APIView):
	"""View to render all products"""

	service = ProductsGetService()
	serializer_class = ProductSerializer

	def get(self, request):
		all_products = self.service.get_all()
		serializer = self.serializer_class(all_products, many=True)
		return Response(serializer.data)
