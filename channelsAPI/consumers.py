# consumers.py
from django.contrib.auth import get_user_model
from user.serializers import *
from investment.serializers import *
from investment.models import *
from rest_framework import status

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
                    DeleteModelMixin,
                    GenericAsyncAPIConsumer):
    serializer_class = AssetsSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self, **kwargs):
        if kwargs['action'] in ['list']:
            return Asset.objects.filter(is_public=True)


# ws://localhost:8000/virtualcoin/ws/v1/notification
class NotificationConsumer(ListModelMixin,
                           PatchModelMixin,
                           GenericAsyncAPIConsumer):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, **kwargs):
        return Notification.objects.filter(user=self.scope['user'], is_ack=False)
