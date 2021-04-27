from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Wallet
from rest_framework import mixins


class WalletViewSet(mixins.RetrieveModelMixin):
    def get_queryset(self):
        wallet, created = Wallet.objects.get_or_create(owner=self.request.user)
        return wallet
