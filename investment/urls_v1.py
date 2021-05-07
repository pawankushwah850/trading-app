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
from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'^wallet', views.WalletViewSet, basename='wallet')
router.register(r'^assets', views.AssetsViewSet, basename='assets_view_set')
router.register(r'^investments', views.InvestmentViewSet, basename='assets_view_set')
router.register(r'^post-listing', views.MarketListingViewSet, basename='market_listing')
router.register(r'^post-listing/<int:id>', views.MarketListingViewSet, basename='market_listing')
# router.register(r'^trade', views.TradeView, basename='TradeRead')
# router.register(r'^trade/<int:id>', views.TradeView, basename='TradeRead')

urlpatterns = [
    #
]
urlpatterns += router.urls
