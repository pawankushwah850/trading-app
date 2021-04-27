from django.db import models


class Wallet(models.Model):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, unique=True)
    balance = models.FloatField(default=0)


class Assets(models.Model):
    name = models.CharField(max_length=244)
    icon = models.ImageField()
    price = models.FloatField()

# class Investment(models.Model):
#     asset = models.ForeignKey("investment.Assets", on_delete=models.RESTRICT)
#     purchased_price = models.FloatField()
#     purchased_quantity = models.FloatField()
#     purchased_at = models.DateTimeField(auto_now_add=True)
#
#     @property
#     def total_investment(self):
#         return self.purchased_price * self.purchased_quantity
#
#     @property
#     def total_value(self):
#         return self.purchased_quantity * self.asset.price
#
#     @property
#     def profit_and_loss(self):
#         return self.total_investment - self.total_value
#
#
# class MarketListing(models.Model):
#     POST_TYPE_CHOICES = {
#         'BUY': 'BUY',
#         'SELL': 'SELL'
#     }
#     post_type = models.CharField(choices=POST_TYPE_CHOICES)
#     assets_to_trade = models.ManyToManyField('investment.Assets', related_name='assets_to_trade')
#     accepted_coins = models.ManyToManyField('investment.Assets', related_name='accepted_coins')
#     traded_coins = models.FloatField(default=0)
#     remaining_coins = models.FloatField(default=0)
#     partial_binding = models.BooleanField(default=False)
#     accepts_coin_trading = models.BooleanField(default=False)
#     accepts_money_transaction = models.BooleanField(default=False)
#     has_stop_condition = models.BooleanField(default=False)
#     expiry = models.DateTimeField()
#     has_stop_loss_range = models.BooleanField(default=False)
#     stop_loss_high = models.FloatField()
#     stop_loss_low = models.FloatField()
#
#
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
