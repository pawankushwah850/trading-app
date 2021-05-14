from rest_framework.viewsets import ModelViewSet
from .models import *
from user.models import *
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from ExtraServices.Pagination import CustomPaginationInvestment
from django.db import transaction


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
        if self.action in ['list', 'retrieve']:
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
        print(request)
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
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super(MarketListingViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        if self.action == "list" or self.action == "retrieve":
            return MarketListing.objects.filter(is_trade=False).order_by('-pk')
        return MarketListing.objects.all().order_by('-pk')

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('post_type') == "SELL":
            asset_instance = serializer.validated_data.get('assets_to_trade')
            investment_instance = Investment.objects.filter(owner=request.user, asset__id=asset_instance.id)
            # print(investment_instance.values('pk', 'asset__name', 'purchased_quantity'))
            number_of_investment = investment_instance.count()
            if number_of_investment < 1:
                raise serializers.ValidationError(f"No {asset_instance.name} Investment found ")
            elif (list(investment_instance.values('purchased_quantity'))[0].get('purchased_quantity') < 1):
                raise serializers.ValidationError(
                    f"You dont have enough quantity to make post of {asset_instance.name}!")

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(postOwner=self.request.user)

    @action(detail=False, methods=['get'])
    def sell(self, request, pk=None):
        data = MarketListing.objects.filter(post_type="SELL", is_trade=False).order_by('-posted_at')
        serializers = MarketListingSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def buy(self, request, pk=None):
        data = MarketListing.objects.filter(post_type="BUY", is_trade=False).order_by('-posted_at')
        serializers = MarketListingSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class TradingViewSet(ModelViewSet, InvestmentViewSet):
    pagination_class = CustomPaginationInvestment
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super(TradingViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        if self.request.method == "GET":
            return Trading.objects.filter(TradeOwner=self.request.user).order_by('-pk')
        return Trading.objects.all().order_by('-pk')

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TradingSerializerRead
        else:
            return TradingSerializerWrite

    @action(methods=['POST'], detail=False)
    def buy(self, request):

        serializer = TradingSerializerBuySell(data=request.data)
        serializer.is_valid(raise_exception=True)

        postId = serializer.data.get('postId')
        cash = float(serializer.validated_data.get('cash'))
        walletInstance = Wallet.objects.get(owner=self.request.user.id)

        try:
            instance = MarketListing.objects.get(pk=postId)
        except MarketListing.DoesNotExist:
            return serializers.ValidationError(f"This {postId} not found")
        except Exception as error:
            return serializers.ValidationError(error)
        if instance.postOwner == request.user:
            raise serializers.ValidationError("you cannot trade on own post")
        elif instance.post_type != "SELL":
            raise serializers.ValidationError("you can trade only sell type of post")
        elif instance.is_trade == True:
            return serializers.ValidationError("Trading is already done by others.")
        elif instance.total_price > cash:
            return serializers.ValidationError(f"Cash is too low then assets price. Excepted {instance.total_price}")
        elif walletInstance.balance < instance.total_price:
            return serializers.ValidationError("Please recharge your wallet balance")
        else:
            tradingInstance = Trading.objects.create(
                postId=serializer.validated_data['postId'],
                TradeOwner=request.user,
                quantity=serializer.validated_data['quantity'],
                cash=serializer.validated_data['cash'],
            )

            walletInstance.balance -= instance.total_price
            walletInstanceClient = Wallet.objects.get(owner=instance.postOwner.id)
            walletInstanceClient.balance += instance.total_price

            try:
                with transaction.atomic():
                    tradingInstance.save()
                    instance.is_trade = True
                    instance.save()
                    walletInstance.save()
                    walletInstanceClient.save()
            except Exception as error:
                raise serializers.ValidationError(error)

            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['asset_quantity'] = serializer.validated_data['quantity']
            request.data['asset_id'] = instance.assets_to_trade_id

            request.data._mutable = _mutable
            request.data._mutable = False

            with transaction.atomic():
                response_buy = InvestmentViewSet.buy(self, request)
                request.user = instance.postOwner
                response_sell = InvestmentViewSet.sell(self, request)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=False)
    def sell(self, request):

        serializer = TradingSerializerBuySell(data=request.data)
        serializer.is_valid(raise_exception=True)

        postId = serializer.data.get('postId')
        try:
            instance = MarketListing.objects.get(pk=postId)
        except Exception as error:
            raise serializers.ValidationError(error)

        if instance.postOwner == request.user:
            raise serializers.ValidationError("you cannot trade on own post")
        elif instance.post_type != "BUY":
            raise serializers.ValidationError("you can only trade only buy type post")

        elif instance.is_trade == True:
            raise serializers.ValidationError("Trading already done by other")

        investment_instance = Investment.objects.filter(owner=request.user, asset__id=instance.assets_to_trade_id)
        # print(investment_instance.values('pk', 'asset__name', 'purchased_quantity'))
        number_of_investment_quantity = investment_instance.count()

        if number_of_investment_quantity < 1:
            raise serializers.ValidationError("sorry!,You not have asset to sell")

        elif list(investment_instance.values('purchased_quantity'))[0].get('purchased_quantity') < 1:
            raise serializers.ValidationError("sorry!,You not have asset quantity to sell")

        asset_price = instance.total_price
        # trader
        wallet_balance_instance = Wallet.objects.get(owner=request.user)

        # postowner
        walletInstanceClient = Wallet.objects.get(owner=instance.postOwner_id)

        if walletInstanceClient.balance < asset_price:
            raise serializers.ValidationError('Client not have enough balance to buy!')
        else:
            tradingInstance = Trading.objects.create(
                postId=serializer.validated_data['postId'],
                TradeOwner=request.user,
                quantity=serializer.validated_data.get('quantity', 1),
                cash=asset_price
            )

            wallet_balance_instance.balance += asset_price
            walletInstanceClient.balance -= asset_price

            try:
                with transaction.atomic():
                    tradingInstance.save()
                    instance.is_trade = True
                    instance.save()
                    wallet_balance_instance.save()
                    walletInstanceClient.save()
            except Exception as error:
                raise serializers.ValidationError(error)

            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['asset_quantity'] = serializer.validated_data.get('quantity', 1)
            request.data['asset_id'] = instance.assets_to_trade_id
            request.data._mutable = _mutable
            request.data._mutable = False

            with transaction.atomic():
                response_sell = InvestmentViewSet.sell(self, request)
                request.user = instance.postOwner
                response_buy = InvestmentViewSet.buy(self, request)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

# todo in buy trading user can trade only when investment.purchased_quantity have enough quantity & socket fetching
# custom_admin side graph & payment gateway
# code reuseable
