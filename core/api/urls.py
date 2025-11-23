from django.urls import path
from .views import (
    ItemDetailView, 
    OrderDetailView, 
    CreateStripeSessionView, 
    CreateOrderStripeSessionView, 
    ItemListView, 
    OrderListView,
    CreatePaymentIntentView,
    health_check
)

urlpatterns = [
    path('', health_check, name='health-check'), 
    path('items/', ItemListView.as_view(), name='item-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    
    # Checkout Session
    path('buy/<int:id>/', CreateStripeSessionView.as_view(), name='buy-item'),
    path('buy_order/<int:id>/', CreateOrderStripeSessionView.as_view(), name='buy-order'),
    
    # Payment Intent (Custom Flow)
    path('buy/intent/<int:id>/', CreatePaymentIntentView.as_view(), name='buy-intent'),
    
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
