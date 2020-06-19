from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tickets_app import views

router = DefaultRouter()
router.register(r'create/event', views.HostEventViewSet, basename='host_event_api')
router.register(r'create/wallet', views.HostWalletViewSet, basename='host_wallet_api')
router.register(r'create/ticket', views.HostTicketViewSet, basename='host_ticket_api')
router.register(r'get/events', views.ClientEventViewSet, basename='client_events_api')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
