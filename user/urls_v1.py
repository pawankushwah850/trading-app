from django.urls import path
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'^users', views.UserViewSet, basename='users')
router.register(r'^profile', views.ProfileViewset, basename='users-profile')


urlpatterns = [
    path('auth/login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls
