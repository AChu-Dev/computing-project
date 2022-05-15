from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
        path('auth/', obtain_auth_token),

        path("duser/list/", views.duser_list_view),
        path("duser/list/<int:pk>/", views.duser_detail_view),
        path("duser/create2/", views.create_user_django),

        path("resort/", views.resort_api_view),
        path("resort/<int:pk>/", views.resort_api_id_view),

        path("favourite/create/", views.favourite_create_view),
        path('favourite/detail/<int:pk>/', views.favourite_detail_view),
        path('favourite/list/', views.favourite_list_view),
        path('favourite/list/user/', views.favourite_list_user),
        path('favourite/list/resort/', views.favourite_list_resort),
        path("favourite/<int:pk>/", views.favourite_api_id_view),

        path('signin/', views.signin),
        path('signout/', views.signout),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ]
