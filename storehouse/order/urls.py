from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order import views

router = DefaultRouter()
router.register(r'order_item', views.OrderItemViewSet, basename="orderitem")
router.register(r'order', views.OrderViewSet, basename="order")


urlpatterns = [
    path('', include(router.urls)),
]
