from rest_framework import serializers
from investment.models import Wallet, Asset, Investment, InvestmentOrders, MarketListing


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['name', 'icon', 'price']


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
    class Meta:
        model = MarketListing
        fields = ['post_type', 'assets_to_trade', 'accepted_coins', 'partial_binding', 'accepts_coin_trading',
                  'accepts_money_transaction', 'has_stop_condition', 'expiry', 'stop_loss_high', 'stop_loss_low',]

    def validate_assets_to_trade(self, attrs):
        user = self.context.get("request").user
        investments = Investment.objects.filter(owner=user)
        investment_assets = []
        for investment in investments:
            investment_assets.append(investment.asset)
        for asset in attrs:
            if asset in investment_assets:
                investment = investments.filter(asset=asset)

            else:
                raise serializers.ValidationError("Assets is not in your investment")

