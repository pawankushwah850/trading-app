from rest_framework import serializers
from investment.models import *
from django.contrib.auth import get_user_model
from rest_framework.response import Response


# Trade


class WalletSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Wallet
        fields = ['owner', 'balance']


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
    assets_to_trade = AssetsSerializer(read_only=True)
    postOwner = serializers.ReadOnlyField(source='postOwner.email')

    class Meta:
        model = MarketListing
        fields = (
            'pk', 'postOwner', 'post_type', 'assets_to_trade', 'accepted_coins', 'traded_coins', 'remaining_coins',
            'partial_binding', 'accepts_coin_trading', 'accepts_money_transaction', 'has_stop_condition',
            'expiry', 'has_stop_loss_range', 'stop_loss_high', 'stop_loss_low', 'posted_at', 'total_price',)


class MarketListingSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = MarketListing
        fields = ('pk', 'post_type', 'assets_to_trade', 'accepted_coins', 'traded_coins', 'remaining_coins',
                  'partial_binding', 'accepts_coin_trading', 'accepts_money_transaction', 'has_stop_condition',
                  'expiry', 'has_stop_loss_range', 'stop_loss_high', 'stop_loss_low', 'posted_at',)

    '''
    If “Is Stop Condition Set” boolean is set
        to True, then expiry and Stop price low
        are required.
        If “Is Stop Price Range” boolean is set to
        True, then “Stop Price Low” and “Stop
        Price High” are required
        Stop Price Low < Stop Price High
    '''

    def validate(self, attrs):

        expiry = attrs.get('expiry', "")
        stopLowLoss = attrs.get('stop_loss_low', "")
        stopHighLoss = attrs.get('stop_loss_high', "")

        if attrs.get('has_stop_condition') == True:
            if (expiry == "" or expiry == None or stopLowLoss == "" or stopLowLoss == None):
                raise serializers.ValidationError('expiry and stop loss low are required! ')
        elif attrs.get('has_stop_loss_range') == True:
            if (stopLowLoss == "" or stopLowLoss == None or stopHighLoss == "" or stopHighLoss == None):
                raise serializers.ValidationError('This field must be an even number.')
            elif (stopLowLoss > stopHighLoss):
                raise serializers.ValidationError("stop loss low must be less then stop low high")
            else:
                pass

        return attrs


class TradingSerializerRead(serializers.ModelSerializer):
    TradeOwner = serializers.ReadOnlyField(source='TradeOwner.email')
    postId = MarketListingSerializer(read_only=True)

    class Meta:
        model = Trading
        fields = ('pk', 'TradeOwner', 'quantity', 'cash', 'postId', 'tradingDate',)


class TradingSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = Trading
        fields = ('pk', 'quantity', 'cash', 'postId', 'tradingDate',)


class TradingSerializerBuySell(serializers.Serializer):
    postId = serializers.PrimaryKeyRelatedField(queryset=MarketListing.objects.all(), required=True)
    cash = serializers.FloatField(required=False)
    quantity = serializers.FloatField(required=False)
