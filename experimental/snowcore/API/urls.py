from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'Users', views.UserViewSet)
#router.register(r'User Create', views.user_create_view)
#router.register(r'User get Details', views.user_detail_view)
#router.register(r'User List', views.user_list_view)
#router.register(r'api_home', views.api_home)
#router.register(r'Users2', views.SingleUserView)

urlpatterns = [
        path('user/create/', views.user_create_view),
        path('user/detail/<int:pk>', views.user_detail_view),
        path('user/list/', views.user_list_view),
        path('user/update/<int:pk>', views.user_update_view),
        path('user/delete/<int:pk>', views.user_delete_view),
        path('resort/create/', views.resort_create_view),
        path('resort/detail/<int:pk>', views.resort_detail_view),
        path('resort/list/', views.resort_list_view),
        # TESTING URLs
        path('', include(router.urls)),
        path('test_api/', views.api_post),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        ]
