"""snowcore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.conf import include
from users import views as user_views

from rest_framework.routers import DefaultRouter
from API.views import UserAPIViewSet, ResortAPIViewSet, FavouriteAPIViewSet

router = DefaultRouter()
router.register("User Router", UserAPIViewSet, basename="User API")
router.register("Resort Router", ResortAPIViewSet, basename="Resort API")
router.register("Favourite Router", FavouriteAPIViewSet, basename="Resort API")



urlpatterns = [
    path('admin/', admin.site.urls),
#    path('register/', user_views.register, name='register'),
#    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
#    path('api/', auth_views.LogoutView.as_view(template_name="users/api.html"), name='api'),
    path('rest_api/', include('API.urls')),
    path('API/', include(router.urls))
]
