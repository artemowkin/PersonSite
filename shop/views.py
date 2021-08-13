from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import ProductsGetService, ProductUpdateService
from .services.facades import ProductCRUDFacade, ProductReviewCRUDFacade
from .serializers import ProductSerializer, ProductReviewSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	facade_class = ProductCRUDFacade


class ConcreteProductView(BaseConcreteView):
	"""View to render a concrete product"""

	facade_class = ProductCRUDFacade

class ProductImageUploadView(BaseUploadImageView):
	"""View to upload image for product entry"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()


class AllProductReviewsView(BaseAllCreateView):
	"""View to render all product reviews and create a new"""

	permission_classes = [IsAuthenticatedOrReadOnly]
	facade_class = ProductReviewCRUDFacade

	def create_facade(self):
		product_pk = self.kwargs['pk']
		return self.facade_class(product_pk)

	def dispatch(self, request, pk):
		return super().dispatch(request)


class ConcreteProductReviewView(BaseConcreteView):
	"""View to render a concrete product review, update and delete it"""

	permission_classes = [IsAuthenticatedOrReadOnly]
	facade_class = ProductReviewCRUDFacade

	def create_facade(self):
		product_pk = self.kwargs['product_pk']
		return self.facade_class(product_pk)

	def dispatch(self, request, product_pk, review_pk):
		return super().dispatch(request, review_pk)
