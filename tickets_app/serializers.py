from rest_framework import serializers
from . import models


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ['__all__']


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['__all__']


class EventSerializer(serializers.ModelSerializer):
    tickets = serializers.StringRelatedField(many=True)
    event_host = serializers.StringRelatedField()

    class Meta:
        model = models.Event
        fields = ['description', 'name', 'date', 'slug', 'tickets', 'event_host']


class HostWalletSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        wallet_type = validated_data.pop('wallet_type')
        wallet_id = validated_data.pop('wallet_id')
        event_host = validated_data.pop('event_host')

        # raising error cause of model's singleton
        if event_host.wallets:
            raise serializers.ValidationError('У вас уже есть привязанный счет, удалите и попробуйте снова')
        else:
            wallet = models.Ticket.objects.create(wallet_type=wallet_type, wallet_id=wallet_id)
            return wallet

    class Meta:
        model = models.Wallet
        fields = ['wallet_type', 'wallet_id']


class HostTicketSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        ticket_type = validated_data.pop('ticket_type')
        event = validated_data.pop('event')
        ticket_count = validated_data.pop('ticket_count')
        event_host = validated_data.pop('event_host')

        # raising error if attach to wrong event
        if event.event_host != event_host:
            raise serializers.ValidationError('Мероприятие не ваше, введите верные данные')
        else:
            ticket = models.Ticket.objects.create(ticket_type=ticket_type, event=event, ticket_count=ticket_count,
                                                  event_host=event_host)
            return ticket

    class Meta:
        model = models.Ticket
        fields = ['ticket_type', 'event', 'ticket_count']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    cart_item = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Cart
        fields = ['user', 'cart_item', 'status']


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CartItem
        fields = '__all__'
