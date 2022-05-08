from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
        path('auth/', obtain_auth_token),
        path('user/list/', views.user_list_view),
        path('user/create/', views.user_create_view),
        path('<int:pk>/detail/', views.user_detail_view),
        path('<int:pk>/user/update/', views.user_update_view),
        path('<int:pk>/admin/update/', views.user_update_mixin),
        path('<int:pk>/user/delete/', views.user_delete_view),

        path('resort/create/', views.resort_create_view),
        path('<int:pk>/resort/detail/', views.resort_detail_view),
        path('<int:pk>/resort/update/', views.resort_update_view),
        path('<int:pk>/resort/delete/', views.resort_delete_view),
        path('resort/list/', views.resort_list_view),

        path('favourite/create/', views.favourite_create_view),
        path('<int:pk>/favourite/detail/', views.favourite_detail_view),
        path('<int:pk>/favourite/update/', views.favourite_update_view),
        path('<int:pk>/favourite/delete/', views.favourite_delete_view),
        path('favourite/list/', views.favourite_list_view),
        # List of favourite resorts by user
        # Number of favourties for a specific resort
        # TESTING URLs
        path('test_api/', views.api_post),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ]