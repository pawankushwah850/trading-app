from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from functools import reduce


class Wallet(models.Model):
    owner = models.OneToOneField('user.User', on_delete=models.CASCADE)
    balance = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Wallets"

    def __str__(self):
        return self.owner.email


class Asset(models.Model):
    name = models.CharField(max_length=244)
    icon = models.ImageField()
    price = models.FloatField()
    is_public = models.BooleanField(default=True)

    # todo availabel coin and asset quantity

    def __str__(self):
        return self.name

    def __unicode__(self):
        return '%d: %s' % (self.name, self.price)

    @property
    def live_price(self):
        # todo read from live stream probably
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

    class Meta:
        verbose_name_plural = "Investment Orders"

    def __str__(self):
        return self.owner.email


class MarketListing(models.Model):
    POST_TYPE_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]
    post_type = models.CharField(choices=POST_TYPE_CHOICES, max_length=10)
    assets_to_trade = models.ForeignKey('investment.Asset', on_delete=models.CASCADE, related_name='assets_to_trade')
    accepted_coins = models.ManyToManyField('investment.Asset', related_name='accepted_coins')  # todo coin
    traded_coins = models.FloatField(default=0)  # todo trade coin
    remaining_coins = models.FloatField(default=0)  # todo remaining coin
    partial_binding = models.BooleanField(default=False)
    accepts_coin_trading = models.BooleanField(default=False)
    accepts_money_transaction = models.BooleanField(default=False)
    has_stop_condition = models.BooleanField(default=False)
    expiry = models.DateTimeField()
    has_stop_loss_range = models.BooleanField(default=False)
    stop_loss_high = models.FloatField()
    stop_loss_low = models.FloatField()
    postOwner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    is_trade = models.BooleanField(default=False, verbose_name="is_trade",
                                   help_text="Its means trading done or not in this post.")
    posted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post_type

    def clean(self):
        if self.has_stop_condition == True:
            if ((self.expiry == "" or self.expiry == None) and (
                    self.stop_loss_low == "" or self.stop_loss_low == None)):
                raise ValidationError("expire And stop loss low value are required!")
        elif self.has_stop_loss_range == True:
            if ((self.stop_loss_high == "" or self.stop_loss_high == None) and (
                    self.stop_loss_low == "" or self.stop_loss_low == None)):
                raise ValidationError("stop_loss_high And stop loss low value are required!")
            elif (self.stop_loss_low > self.stop_loss_high):
                raise ValidationError("Stop low loss must be less then high!")

    @property
    def total_price(self):
        price = self.assets_to_trade.price
        return price


class Trading(models.Model):
    TradeOwner = models.ForeignKey('user.User', on_delete=models.CASCADE)
    postId = models.ForeignKey('investment.MarketListing', on_delete=models.CASCADE, related_name="tradeId")
    quantity = models.FloatField(verbose_name="quantity", default=0)
    cash = models.FloatField(verbose_name='cash', default=0)
    tradingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postId.post_type

    class Meta:
        verbose_name_plural = "Trading"
