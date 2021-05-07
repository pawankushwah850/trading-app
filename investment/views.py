from django.db.models.lookups import In
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Wallet, Asset, Investment, MarketListing
# Trade
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import WalletSerializers, AssetsSerializer, InvestmentSerializer, \
    InvestmentBuySellSerializer, MarketListingSerializer, MarketListingSerializerWrite  # , \
# TradeRead, TradeWrite
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated, IsAdminUser
from rest_framework import status
from ExtraServices.Pagination import CustomPaginationInvestment


class WalletViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = WalletSerializers
    pagination_class = CustomPaginationInvestment

    def get_queryset(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return Wallet.objects.filter(id=wallet.id)


class AssetsViewSet(ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetsSerializer
    pagination_class = CustomPaginationInvestment

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class InvestmentViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = InvestmentSerializer
    pagination_class = CustomPaginationInvestment

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


# @action(methods=['GET', 'POST', 'DELETE', 'PUT'], detail=True)
class MarketListingViewSet(ModelViewSet):
    queryset = MarketListing.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPaginationInvestment

    def get_serializer_context(self):
        context = super(MarketListingViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MarketListingSerializer
        return MarketListingSerializerWrite

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('successfully deleted', status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(postOwner=self.request.user)

    @action(detail=False, methods=['get'])
    def sell(self, request):
        data = MarketListing.objects.filter(post_type="SELL")
        serializers = MarketListingSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def buy(self, request):
        data = MarketListing.objects.filter(post_type="BUY")
        serializers = MarketListingSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

# @action(methods=['GET', 'POST', 'PUT', 'DELETE'], detail=True)
# class TradeView(ModelViewSet):
#     queryset = Trade.objects.all()
#     permission_classes = (IsAuthenticated,)
#     pagination_class = CustomPaginationInvestment
#
#     def get_serializer_context(self):
#         context = super(TradeView, self).get_serializer_context()
#         context.update({"request": self.request})
#         return context
#
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return TradeRead
#         return TradeWrite
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response('successfully deleted', status=status.HTTP_200_OK)
#
#     def update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         return super().update(request, *args, **kwargs)
