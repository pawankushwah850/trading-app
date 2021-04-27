from rest_framework import serializers
from investment.models import Wallet, Asset, Investment


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
