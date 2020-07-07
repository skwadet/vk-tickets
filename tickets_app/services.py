from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models


# TODO
class AuthenticatedHostCreate(viewsets.ModelViewSet):
    model = None
    model_serializer = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(event_host=self.request.user.id)

    def get_serializer_class(self):
        serializer = self.model_serializer
        return serializer

    def perform_create(self, serializer):
        serializer.save(event_host=self.request.user)


class AuthenticatedUserCartItemCRUD(AuthenticatedHostCreate):
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        buyer = self.request.user
        cart_exists = models.Cart.objects.filter(user=buyer).exists()
        if cart_exists:
            serializer.save(user=buyer, cart=buyer.user_cart)
        else:
            new_cart = models.Cart.objects.create(user=buyer)
            print(new_cart)
            serializer.save(user=buyer, cart=new_cart)


class QuerySetGetAllItems:
    @staticmethod
    def get_queryset(model):
        queryset = model.objects.all()
        return queryset
