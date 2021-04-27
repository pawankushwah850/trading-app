from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from . import serializers
from . import models as user_models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt import views
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = user_models.User.objects.all()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        if request.data.get('email'):
            try:
                user = user_models.User.objects.get(email__iexact=request.data.get('email'))
            #     todo send forget password email
            except user_models.User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"email": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
