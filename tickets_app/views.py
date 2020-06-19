from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from . import mixins
from . import models
from . import serializers


# <!___________________________!>
class HostEventViewSet(mixins.AuthenticatedModelViewSetAPI):
    model = models.Event
    model_serializer = serializers.EventSerializer


class HostWalletViewSet(mixins.AuthenticatedModelViewSetAPI):
    model = models.Wallet
    model_serializer = serializers.HostWalletSerializer


class HostTicketViewSet(mixins.AuthenticatedModelViewSetAPI):
    model = models.Ticket
    model_serializer = serializers.HostTicketSerializer
# <!___________________________!>


class ClientEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer

    @action(detail=True, methods=['GET'])
    def buy_ticket(self, request, pk=None, *args, **kwargs):
        event = self.get_object()
        serializer = serializers.EventSerializer(event)
        return Response({'status': serializer.data})


class CartViewSet(mixins.AuthenticatedCartModelViewSetAPI):
    model = models.CartItem
    model_serializer = serializers.CartSerializer
