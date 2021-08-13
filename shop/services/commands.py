from generic.services.commands import BaseGetAllCommand, BaseCreateCommand

from .base import ProductsGetService, ProductCreateService
from ..serializers import ProductSerializer


class GetAllProductsCommand(BaseGetAllCommand):
	"""Command to get all products"""

	get_service_class = ProductsGetService
	serializer_class = ProductSerializer


class CreateProductCommand(BaseCreateCommand):
	"""Command to create a new product"""

	create_service_class = ProductCreateService
	serializer_class = ProductSerializer
