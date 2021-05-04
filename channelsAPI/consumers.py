# consumers.py
from django.contrib.auth import get_user_model
from VirtualCoin.user.serializers import UserSerializer

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    RetrieveModelMixin,
)
from djangochannelsrestframework.permissions import AllowAny


class UserConsumer(RetrieveModelMixin, GenericAsyncAPIConsumer):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
