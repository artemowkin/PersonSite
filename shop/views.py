from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from generic.views import (
	BaseAllCreateView, BaseConcreteView, BaseUploadImageView
)
from .services.base import ProductsGetService, ProductUpdateService
from .services.facades import (
	ProductGetFacade, ProductCreateFacade, ProductUpdateFacade,
	ProductDeleteFacade, ProductReviewGetFacade, ProductReviewCreateFacade,
	ProductReviewUpdateFacade, ProductReviewDeleteFacade
)
from .serializers import ProductSerializer, ProductReviewSerializer


class AllCreateProductsView(BaseAllCreateView):
	"""View to render all products"""

	get_facade_class = ProductGetFacade
	create_facade_class = ProductCreateFacade


class ConcreteProductView(BaseConcreteView):
	"""View to render a concrete product"""

	get_facade_class = ProductGetFacade
	update_facade_class = ProductUpdateFacade
	delete_facade_class = ProductDeleteFacade

class ProductImageUploadView(BaseUploadImageView):
	"""View to upload image for product entry"""

	get_service = ProductsGetService()
	update_service = ProductUpdateService()


class AllProductReviewsView(BaseAllCreateView):
	"""View to render all product reviews and create a new"""

	permission_classes = [IsAuthenticatedOrReadOnly]
	get_facade_class = ProductReviewGetFacade
	create_facade_class = ProductReviewCreateFacade

	def setup_facades(self):
		product_pk = self.kwargs['pk']
		self.get_facade = self.get_facade_class(product_pk)
		self.create_facade = self.create_facade_class(product_pk)

	def dispatch(self, request, pk):
		return super().dispatch(request)


class ConcreteProductReviewView(BaseConcreteView):
	"""View to render a concrete product review, update and delete it"""

	permission_classes = [IsAuthenticatedOrReadOnly]
	get_facade_class = ProductReviewGetFacade
	update_facade_class = ProductReviewUpdateFacade
	delete_facade_class = ProductReviewDeleteFacade

	def setup_facades(self):
		product_pk = self.kwargs['product_pk']
		self.get_facade = self.get_facade_class(product_pk)
		self.update_facade = self.update_facade_class(product_pk)
		self.delete_facade = self.delete_facade_class(product_pk)

	def dispatch(self, request, product_pk, review_pk):
		return super().dispatch(request, review_pk)
