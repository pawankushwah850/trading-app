from rest_framework import serializers
from investment.models import Wallet


class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        field = '__all__'
