
from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'^wallet', views.WalletViewSet, basename='wallet')
router.register(r'^assets', views.AssetsViewSet, basename='assets_view_set')
router.register(r'^investments', views.InvestmentViewSet, basename='assets_view_set')
router.register(r'^post-listing', views.MarketListingViewSet, basename='market_listing')
router.register(r'^post-listing/<int:id>', views.MarketListingViewSet, basename='market_listing')
router.register(r'^post-listing/sell', views.MarketListingViewSet, basename='market_listing-sell')
router.register(r'^post-listing/sell/<int:id>', views.MarketListingViewSet, basename='market_listing-sell')
router.register(r'^post-listing/buy', views.MarketListingViewSet, basename='market_listing-buy')
router.register(r'^post-listing/buy/<int:id>', views.MarketListingViewSet, basename='market_listing-buy')
router.register(r'^trading', views.TradingViewSet, basename='Trading')
router.register(r'^trading/sell', views.TradingViewSet, basename='Trading-sell')
router.register(r'^trading/buy', views.TradingViewSet, basename='Trading-buy')
# router.register(r'^trade/<int:id>', views.TradeView, basename='TradeRead')

urlpatterns = [
    #
]
urlpatterns += router.urls
