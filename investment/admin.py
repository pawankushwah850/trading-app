from django.contrib import admin
from investment.models import *

# Register your models here.

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Wallet._meta.fields]


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Asset._meta.fields]


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Investment._meta.fields]


@admin.register(InvestmentOrders)
class InvestmentOrdersAdmin(admin.ModelAdmin):
    list_display = [f.name for f in InvestmentOrders._meta.fields]


@admin.register(MarketListing)
class MarketListingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MarketListing._meta.fields]


@admin.register(Trade)
class ITradeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Trade._meta.fields]
