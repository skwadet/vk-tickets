from rest_framework import viewsets

from . import models
from . import serializers
from . import services


class HostEventViewSet(services.AuthenticatedHostCreate):
    model = models.Event
    model_serializer = serializers.EventSerializer


class HostWalletViewSet(services.AuthenticatedHostCreate):
    model = models.Wallet
    model_serializer = serializers.HostWalletSerializer


class HostTicketViewSet(services.AuthenticatedHostCreate):
    model = models.Ticket
    model_serializer = serializers.HostTicketSerializer


class ClientEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = services.AllItemsFromQueryset.get_queryset(models.Event)
    serializer_class = serializers.EventSerializer


class CartItemViewSet(services.AuthenticatedUserCartItemCRUD):
    model = models.CartItem
    model_serializer = serializers.CartItemSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = services.AllItemsFromQueryset.get_queryset(models.Cart)
    serializer_class = serializers.CartSerializer
