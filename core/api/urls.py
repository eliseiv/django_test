from django.urls import path
from .views import ItemDetailView, OrderDetailView, CreateStripeSessionView, CreateOrderStripeSessionView, ItemListView, health_check

urlpatterns = [
    path('', health_check, name='health-check'), # Root URL for Docker Healthcheck
    path('items/', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('buy/<int:id>/', CreateStripeSessionView.as_view(), name='buy-item'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('buy_order/<int:id>/', CreateOrderStripeSessionView.as_view(), name='buy-order'),
]
