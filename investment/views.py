from django.db.models.lookups import In
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Wallet, Asset, Investment, MarketListing
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import WalletSerializers, AssetsSerializer, InvestmentSerializer, \
    InvestmentBuySellSerializer, MarketListingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated, IsAdminUser


class WalletViewSet(
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = WalletSerializers

    def get_queryset(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return Wallet.objects.filter(id=wallet.id)


class AssetsViewSet(ModelViewSet):
    serializer_class = AssetsSerializer
    queryset = Asset.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class InvestmentViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = InvestmentSerializer

    def get_serializer_context(self):
        context = super(InvestmentViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Investment.objects.all()
        else:
            return Investment.objects.filter(owner=self.request.user, is_active=True)

    @action(detail=False, methods=['post'])
    def buy(self, request):
        ser = InvestmentBuySellSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        asset = ser.validated_data['asset_id']
        investment, created = Investment.objects.get_or_create(owner=request.user, is_active=True,
                                                               asset=ser.validated_data['asset_id'])
        investment.add(ser.validated_data['asset_quantity'], asset.live_price)
        return Response(InvestmentSerializer(investment).data)

    @action(detail=False, methods=['post'])
    def sell(self, request):
        ser = InvestmentBuySellSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        asset = ser.validated_data['asset_id']
        investment, created = Investment.objects.get_or_create(owner=request.user, is_active=True,
                                                               asset=ser.validated_data['asset_id'])
        investment.remove(ser.validated_data['asset_quantity'], asset.live_price)
        return Response(InvestmentSerializer(investment).data)


class MarketListingViewSet(ModelViewSet):
    queryset = MarketListing.objects.all()
    serializer_class = MarketListingSerializer

    def get_serializer_context(self):
        context = super(MarketListingViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context
