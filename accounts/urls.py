from django.urls import path
from dj_rest_auth import views
from dj_rest_auth.registration import views as reg_views


urlpatterns = [
	path('login/', views.LoginView.as_view(), name='rest_login'),
	path('logout/', views.LogoutView.as_view(), name='rest_logout'),
	path('user/', views.UserDetailsView.as_view(), name='rest_user_details'),
	path(
		'registration/', reg_views.RegisterView.as_view(),
		name='rest_register'
	),
]
