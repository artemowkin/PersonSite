from rest_framework.permissions import IsAuthenticated

from generic.views import BaseAllCreateView
from .services.facades import OrderGetFacade, OrderCreateFacade


class AllCreateOrdersView(BaseAllCreateView):
	"""View to render all user orders"""

	permission_classes = [IsAuthenticated]
	get_facade_class = OrderGetFacade
	create_facade_class = OrderCreateFacade

	def setup_facades(self):
		user = self.request.user
		self.get_facade = self.get_facade_class(user)
		self.create_facade = self.create_facade_class()
