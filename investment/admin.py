from django.contrib import admin
from investment.models import *


# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['owner', 'balance']
    search_fields = ('owner__email',)
    list_filter = ('owner__email',)
    ordering = ('balance',)

    fieldsets = (
        (
            ('Wallet'), {'fields': ('owner', 'balance',)}
        ),
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_public']

    search_fields = ('name',)
    list_filter = ('is_public',)
    ordering = ('price',)
    fieldsets = (
        (
            ('Information'), {'fields': ('name', 'price', 'icon', 'is_public',)}
        ),
    )
    change_list_template = "investment/asset.html"


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'asset', 'purchased_quantity', 'Profit_and_loss', 'is_active', 'purchased_at']

    search_fields = ('owner__email', 'asset__name',)
    list_filter = ('purchased_at', 'is_active',)
    ordering = ('purchased_price', 'purchased_quantity',)
    readonly_fields = ['Profit_and_loss', 'purchased_at']
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

    def profit_and_loss(self, instance):
        self.total_investment = instance.purchased_price * instance.purchased_quantity
        print(self.total_investment)
        self.market_price = instance.purchased_quantity * instance.asset.price
        print(self.market_price)
        return self.market_price - self.total_investment


@admin.register(InvestmentOrders)
class InvestmentOrdersAdmin(admin.ModelAdmin):
    list_display = ['owner', 'asset', 'investment', 'price', 'is_completed', 'timestamp']
    search_fields = ('owner__email',)
    list_filter = ('is_completed',)
    readonly_fields = ['pk', 'owner', 'asset', 'timestamp']
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


@admin.register(MarketListing)
class MarketListingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'postOwner', 'post_type', 'is_trade', 'expiry']

    list_filter = ('post_type', 'accepts_coin_trading', 'assets_to_trade', 'is_trade',)
    readonly_fields = ['pk', 'posted_at', 'is_trade']
    ordering = ('expiry', 'is_trade',)
    fieldsets = (
        (
            ('Market information'), {'fields': ('postOwner', 'post_type', 'assets_to_trade', \
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


@admin.register(Trading)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'TradeOwner', 'postId', 'tradingDate', 'cash', 'profit_and_loss']
    search_fields = ('postId', 'TradeOwner',)
    readonly_fields = ['pk']
    ordering = ('tradingDate',)
