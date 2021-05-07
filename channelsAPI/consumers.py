# consumers.py
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer
from investment.serializers import WalletSerializers, AssetsSerializer
from investment.models import Wallet, Asset

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DeleteModelMixin,
    PatchModelMixin,
)
from djangochannelsrestframework.permissions import AllowAny, IsAuthenticated


# ws://localhost:8000/virtualcoin/ws/v1/users
class UserConsumer(ListModelMixin,
                   RetrieveModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   DeleteModelMixin,
                   PatchModelMixin,
                   GenericAsyncAPIConsumer):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


# ws://localhost:8000/virtualcoin/ws/v1/wallet
class WalletConsumer(ListModelMixin,
                     RetrieveModelMixin,
                     CreateModelMixin,
                     UpdateModelMixin,
                     PatchModelMixin,
                     DeleteModelMixin,
                     GenericAsyncAPIConsumer):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializers
    permission_classes = (AllowAny,)


# ws://localhost:8000/virtualcoin/ws/v1/asset
class AssetConsumer(ListModelMixin,
                    RetrieveModelMixin,
                    CreateModelMixin,
                    UpdateModelMixin,
                    PatchModelMixin,
                    DeleteModelMixin,
                    GenericAsyncAPIConsumer):
    queryset = Asset.objects.all()
    serializer_class = AssetsSerializer
    permission_classes = (AllowAny,)
