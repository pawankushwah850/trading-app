"""VirtualCurruncy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions
# urlpatterns = [
#     path('custom_admin/', custom_admin.site.urls),
#     path('v1/', include('user.urls_v1'), name='v1_urls'),
# ]
# urlpatterns = patterns('',
#     (r'^', include('app.urls')),
#     (r'^custom_admin/', include(custom_admin.site.urls)),
# )

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^v1/', include(
                      [path('', include('user.urls_v1'))]
                  )
                      ),
                  url(r'^v1/', include(
                      [path('', include('investment.urls_v1'))]
                  )
                      ),
                  path(
                      'websocktTools/', TemplateView.as_view(template_name="index.html")
                  )
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
