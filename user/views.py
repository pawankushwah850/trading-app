from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from investment.serializers import *
from investment.models import *
from rest_framework import generics
from ExtraServices.Pagination import CustomPaginationUser
from secrets import token_hex


class UserRegister(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = SignupSerializers
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPaginationUser

    def get_permissions(self):
        if self.action in ['create', 'reset_password', 'forgot_password']:
            permission_classes = [AllowAny]

        elif self.action in ['list', 'retrieve', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        if request.data.get('email'):
            try:
                user = User.objects.get(email__iexact=request.data.get('email'))
                ForgetPasswordToken.objects.all().delete()
                token_expiry = timezone.now() + timedelta(days=1)
                token = ForgetPasswordToken.objects.create(user=user, token=str(token_hex(5)),
                                                           expire_at=token_expiry)
                return Response({'token': token.token, 'expiry date': token_expiry}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"email": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        ser = ResetPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data['token']
        token.user.set_password(ser.validated_data['new_password'])
        token.user.save()
        return Response({"body": "password reset successfully"}, status=status.HTTP_200_OK)


class ProfileViewset(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    User = get_user_model()

    serializer_class_user = UserSerializer
    serializer_class_wallet = WalletSerializers

    permission_classes = (IsAuthenticated,)

    def get_queryset_user(self):
        return User.objects.filter(pk=self.request.user.id)

    def get_queryset_wallet(self):
        return Wallet.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):

        None_filter_user_queryset = self.get_queryset_user()
        user_queryset = self.filter_queryset(None_filter_user_queryset)
        user_serializer = self.serializer_class_user(user_queryset, many=True)

        if list(None_filter_user_queryset.values('verification_status'))[0].get('verification_status', False) == True:

            wallet_queryset = self.filter_queryset(self.get_queryset_wallet())
            wallet_serializer = self.serializer_class_wallet(wallet_queryset, many=True)

            response = {
                'user_information': user_serializer.data,
                'wallet': wallet_serializer.data
            }
        else:
            response = user_serializer.data

        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(pk=self.request.user.pk)
        serializer = self.serializer_class_user(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('verification_status', False):
            return Response("you cannot modified verification_status self.", status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # todo verified by custom_admin : User can see their profile, their confusion portfolio and listings


class NotificationViewset(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.action in ['list', 'partial_update']:
            return Notification.objects.filter(user=self.request.user)
        return serializers.ValidationError("methods not allowed")

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
