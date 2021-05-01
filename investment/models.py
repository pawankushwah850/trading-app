from django.db import models
from django.db import transaction


class Wallet(models.Model):
    owner = models.OneToOneField('user.User', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    def __str__(self):
        return self.owner.email

class Asset(models.Model):
    name = models.CharField(max_length=244)
    icon = models.ImageField()
    price = models.FloatField()
    is_public = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%d: %s' % (self.name, self.price)

    @property
    def live_price(self):
        #         todo read from live stream probably
        return self.price


class Investment(models.Model):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    asset = models.ForeignKey("investment.Asset", on_delete=models.RESTRICT)
    purchased_price = models.FloatField(default=0)  # todo do we need to average out the price on new buy or sell
    purchased_quantity = models.FloatField(default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.owner.email

    @transaction.atomic
    def add(self, quantity, purchased_price):
        total_quantity_purchased = self.purchased_quantity + quantity
        total_investment_made = self.total_investment + (quantity * purchased_price)

        self.purchased_quantity += quantity
        self.purchased_price = total_investment_made / total_quantity_purchased
        self.save()
        InvestmentOrders.objects.create(asset=self.asset, price=purchased_price,
                                        owner=self.owner, is_completed=True,
                                        investment=self)

    @transaction.atomic
    def remove(self, quantity, purchased_price):
        total_quantity_purchased = self.purchased_quantity - quantity
        total_investment_made = self.total_investment - (quantity * purchased_price)

        self.purchased_quantity -= quantity
        self.purchased_price = total_investment_made / total_quantity_purchased
        self.save()
        InvestmentOrders.objects.create(asset=self.asset, price=purchased_price,
                                        owner=self.owner, is_completed=True,
                                        investment=self)

    @property
    def total_investment(self):
        return self.purchased_price * self.purchased_quantity

    @property
    def total_value(self):
        return self.purchased_quantity * self.asset.price

    @property
    def profit_and_loss(self):
        return self.total_investment - self.total_value


class InvestmentOrders(models.Model):
    asset = models.ForeignKey('investment.Asset', on_delete=models.RESTRICT)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    is_completed = models.BooleanField()
    investment = models.ForeignKey('investment.Investment', null=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.owner.email

class MarketListing(models.Model):
    POST_TYPE_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]
    post_type = models.CharField(choices=POST_TYPE_CHOICES, max_length=10)
    assets_to_trade = models.ManyToManyField('investment.Asset', related_name='assets_to_trade')
    accepted_coins = models.ManyToManyField('investment.Asset', related_name='accepted_coins')
    traded_coins = models.FloatField(default=0)
    remaining_coins = models.FloatField(default=0)
    partial_binding = models.BooleanField(default=False)
    accepts_coin_trading = models.BooleanField(default=False)
    accepts_money_transaction = models.BooleanField(default=False)
    has_stop_condition = models.BooleanField(default=False)
    expiry = models.DateTimeField()
    has_stop_loss_range = models.BooleanField(default=False)
    stop_loss_high = models.FloatField()
    stop_loss_low = models.FloatField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_type

class Trade(models.Model):
    tradeId = models.BigAutoField(primary_key=True)
    purchaseItem = models.ManyToManyField('investment.Asset', related_name="purchaseTradeItem")
    cash = models.FloatField(verbose_name="cash", null=False, blank=True, default=0)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name="created date")

    class Meta:
        ordering = ['createdDate']

    def __str__(self):
        return self.tradeId

# class CoinTransaction(models.Model):
#     TRADE_TYPE_CHOICES = (
#         ('BUY', 'BUY',),
#         ('SELL', 'SELL')
#     )
#     buyer = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='buyer')
#     seller = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='seller')
#     created_at = models.DateTimeField(auto_now_add=True)
#     activity_type = models.CharField(choices=TRADE_TYPE_CHOICES, max_length=5)
#     amount = models.FloatField()
#     total_price = models.FloatField()
