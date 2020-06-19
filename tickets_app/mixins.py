from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


# here host creates events, wallets, tickets and save it by his name
class AuthenticatedModelViewSetAPI(viewsets.ModelViewSet):
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


class AuthenticatedCartModelViewSetAPI(AuthenticatedModelViewSetAPI):
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
