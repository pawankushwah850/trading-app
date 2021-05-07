from rest_framework import serializers
from investment.models import Wallet, Asset, Investment, InvestmentOrders, MarketListing
    # Trade


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['pk', 'name', 'icon', 'price']


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['asset', 'purchased_price', 'purchased_quantity', 'purchased_at', 'total_investment']

    # todo verify the price before creating
    def create(self, validated_data):
        request = self.context.get('request')
        if not request:
            raise Exception('Cant find request in context')
        validated_data['owner'] = request.user
        return super().create(validated_data)


class InvestmentBuySellSerializer(serializers.Serializer):
    asset_id = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())
    asset_quantity = serializers.IntegerField()


class MarketListingSerializer(serializers.ModelSerializer):
    accepted_coins = AssetsSerializer(many=True, read_only=True)
    assets_to_trade = AssetsSerializer(many=True, read_only=True)

    class Meta:
        model = MarketListing
        fields = ('pk', 'post_type', 'assets_to_trade', 'accepted_coins', 'traded_coins', 'remaining_coins',
                  'partial_binding', 'accepts_coin_trading', 'accepts_money_transaction', 'has_stop_condition',
                  'expiry', 'has_stop_loss_range', 'stop_loss_high', 'stop_loss_low', 'posted_at',)


class MarketListingSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = MarketListing
        fields = ('pk', 'post_type', 'assets_to_trade', 'accepted_coins', 'traded_coins', 'remaining_coins',
                  'partial_binding', 'accepts_coin_trading', 'accepts_money_transaction', 'has_stop_condition',
                  'expiry', 'has_stop_loss_range', 'stop_loss_high', 'stop_loss_low', 'posted_at',)


# class TradeRead(serializers.ModelSerializer):
#     purchaseItem = AssetsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Trade
#         fields = (
#             'tradeId', 'purchaseItem', 'cash', 'createdDate',
#         )

#
# class TradeWrite(serializers.ModelSerializer):
#     class Meta:
#         model = Trade
#         fields = (
#             'tradeId', 'purchaseItem', 'cash', 'createdDate',
#         )
