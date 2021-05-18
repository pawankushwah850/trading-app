from django.urls import path
from rest_framework import routers
from . import views
from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'^users', views.UserViewSet, basename='users')
router.register(r'^users/forgot_password', views.UserViewSet, basename='forgot_password')
router.register(r'^users/reset_password', views.UserViewSet, basename='reset_password')
router.register(r'^profile', views.ProfileViewset, basename='users-profile')


urlpatterns = [
    path('auth/login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/signup', views.UserRegister.as_view(), name='signup'),
]
urlpatterns += router.urls
