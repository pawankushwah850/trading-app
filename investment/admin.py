from django.contrib import admin
from investment.models import *

# Register your models here.

IGNORE_FIELD = ['id']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = list_display = sorted([f.name for f in Wallet._meta.fields \
                                             if (f.name not in IGNORE_FIELD)])[::-1]
    search_fields = ('owner__email',)
    list_filter = ('owner',)
    ordering = ('balance',)

    fieldsets = (
        (
            ('Wallet'), {'fields': ('owner', 'balance',)}
        ),
    )


IGNORE_FIELD.append('icon')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = sorted([f.name for f in Asset._meta.fields \
                           if (f.name not in IGNORE_FIELD)])[::-1]

    search_fields = ('name',)
    list_filter = ('is_public',)
    ordering = ('price',)
    readonly_fields = [f.name for f in Asset._meta.fields]
    fieldsets = (
        (
            ('Information'), {'fields': ('name', 'price', 'icon', 'is_public',)}
        ),
    )


IGNORE_FIELD.pop()


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = sorted([f.name for f in Investment._meta.fields \
                           if (f.name not in IGNORE_FIELD)])[::-1]

    search_fields = ('owner__email', 'asset__name',)
    list_filter = ('purchased_at', 'is_active',)
    ordering = ('purchased_price', 'purchased_quantity',)
    readonly_fields = [f.name for f in Investment._meta.fields]
    fieldsets = (
        (
            ('User Information'), {'fields': ('owner', 'asset',)}
        ),
        (
            ('User Purchasing'), {'fields': ('purchased_price', 'purchased_quantity',)}
        ),
        (
            ('Purchase Date and Status'), {'fields': ('purchased_at', 'is_active',)}
        )
    )


@admin.register(InvestmentOrders)
class InvestmentOrdersAdmin(admin.ModelAdmin):
    list_display = sorted([f.name for f in InvestmentOrders._meta.fields \
                           if (f.name not in IGNORE_FIELD)])[::-1]
    search_fields = ('owner__email',)
    list_filter = ('is_completed',)
    readonly_fields = [f.name for f in InvestmentOrders._meta.fields]
    ordering = ('is_completed', 'price',)
    fieldsets = (
        (
            ('User Information'), {'fields': ('owner', 'asset', 'is_completed',)}
        ),
        (
            ('User Investment'), {'fields': ('investment', 'price',)}
        ),
        (
            ('Investment date'), {'fields': ('timestamp',)}
        ),
    )


IGNORE_FIELD.extend(['traded_coins', 'remaining_coins', 'partial_binding', 'accepts_coin_trading', \
                     'accepts_money_transaction', 'has_stop_condition', 'expiry', 'stop_loss_low'
                     ])


@admin.register(MarketListing)
class MarketListingAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MarketListing._meta.fields \
                           if (f.name not in IGNORE_FIELD)]

    list_filter = ('post_type', 'accepts_coin_trading', 'assets_to_trade',)
    readonly_fields = [f.name for f in MarketListing._meta.fields]
    ordering = ('expiry', 'stop_loss_high',)
    fieldsets = (
        (
            ('Market information'), {'fields': ('post_type', 'assets_to_trade', \
                                                'partial_binding', 'accepts_money_transaction',)}
        ),
        (
            ('About Coin Investment'), {'fields': ('accepted_coins', 'traded_coins', \
                                                   'remaining_coins', 'accepts_coin_trading', \
                                                   )}
        ),
        (
            ('Stop Loss'), {'fields': ('has_stop_condition', 'has_stop_loss_range', \
                                       'stop_loss_high', 'stop_loss_low',)}
        ),
        (
            ('Importent Date'), {'fields': ('expiry', 'posted_at',)}
        ),
    )


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = sorted([f.name for f in Trade._meta.fields])[::-1]
    search_fields = ('tradeId',)
    readonly_fields = [f.name for f in Trade._meta.fields]
    ordering = ('createdDate',)