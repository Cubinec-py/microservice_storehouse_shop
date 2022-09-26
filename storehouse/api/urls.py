from django.urls import path, include, re_path
from django.conf import settings

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions

from books.views import BookViewSet, BookItemViewSet, AuthorViewSet, GenreViewSet
from order.views import OrderItemViewSet, OrderViewSet, ShippingAddressViewSet

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = DefaultRouter()
router.register(r'book', BookViewSet, basename="book")
router.register(r'book_instance', BookItemViewSet, basename="bookinstance")
router.register(r'author', AuthorViewSet, basename="author")
router.register(r'genre', GenreViewSet, basename="genre")
router.register(r'order_item', OrderItemViewSet, basename="orderitem")
router.register(r'order', OrderViewSet, basename="order")
router.register(r'shipping_address', ShippingAddressViewSet, basename="shippingaddress")


schema_view = get_schema_view(
    openapi.Info(
        title="STOREHOUSE API",
        default_version="v1",
        description="API for Storehouse application",
    ),
    url=settings.SWAGGER_SETTINGS["DEFAULT_API_URL"],
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_patterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('auth/auth-token', views.obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += swagger_patterns
