from django.urls import path

from . import views


urlpatterns = [
	path('', views.AllCreatePostsView.as_view(), name='all_posts'),
	path('<uuid:pk>/', views.ConcretePostView.as_view(), name='concrete_post'),
	path('<uuid:pk>/preview/<str:filename>/', views.PostPreviewUploadView.as_view(), name='post_preview_view'),
	path('user/<int:user_pk>/', views.UserPostsView.as_view(), name='user_posts'),
]