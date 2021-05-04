from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models as user_models
from . import serializers

from ExtraServices.Pagination import CustomPaginationUser


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = user_models.User.objects.all()
    pagination_class = CustomPaginationUser

    def get_permissions(self):
        if self.action in ['create', 'reset_password', 'forgot_password']:
            permission_classes = [AllowAny]

        elif self.action in ['list', 'retrive', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        if request.data.get('email'):
            try:
                user = user_models.User.objects.get(email__iexact=request.data.get('email'))
                user_models.ForgetPasswordToken.objects.all().delete()
                token = user_models.ForgetPasswordToken.objects.create(user=user,
                                                                       expire_at=timezone.now() + timedelta(days=3))
                print(token.token)
                return Response(status=status.HTTP_200_OK)
            except user_models.User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"email": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def reset_password(self, request):
        ser = serializers.ResetPasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        token = ser.validated_data['token']
        token.user.set_password(ser.validated_data['new_password'])
        token.user.save()
        return Response(status=status.HTTP_200_OK)
