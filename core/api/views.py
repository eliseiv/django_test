from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import stripe

from .models import Item, Order
from .serializers import ItemSerializer, OrderSerializer

# Helper to get correct key locally
def get_stripe_keys(currency):
    if str(currency).lower() == 'eur':
        return settings.STRIPE_PUBLIC_KEY_EUR, settings.STRIPE_SECRET_KEY_EUR
    return settings.STRIPE_PUBLIC_KEY, settings.STRIPE_SECRET_KEY

def get_stripe_api_key(currency):
    _, secret_key = get_stripe_keys(currency)
    return secret_key

def health_check(request):
    return HttpResponse("OK")

class ItemListView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ItemDetailView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CreateStripeSessionView(APIView):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Set API key based on currency
        stripe.api_key = get_stripe_api_key(item.currency)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': item.price,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success'),
                cancel_url=request.build_absolute_uri('/cancel'),
            )
            return Response({'id': session.id})
        except Exception as e:
            print(f"Stripe Error: {e}") 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateOrderStripeSessionView(APIView):
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not order.items.exists():
             return Response({"error": "Order is empty"}, status=status.HTTP_400_BAD_REQUEST)

        currency = order.items.first().currency
        stripe.api_key = get_stripe_api_key(currency)

        line_items = []
        for item in order.items.all():
            if item.currency != currency:
                 return Response({"error": "Mixed currencies in order not supported"}, status=status.HTTP_400_BAD_REQUEST)
            
            line_items.append({
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            })

        stripe_discounts = []
        if order.discount:
            try:
                coupon = stripe.Coupon.create(
                    percent_off=order.discount.percent,
                    duration='once',
                    name=order.discount.name,
                    api_key=stripe.api_key # Pass key explicitly or rely on global
                )
                stripe_discounts.append({'coupon': coupon.id})
            except Exception as e:
                print(f"Error creating coupon: {e}")

        tax_rates = []
        if order.tax:
            try:
                tax_rate = stripe.TaxRate.create(
                    display_name=order.tax.name,
                    inclusive=False,
                    percentage=order.tax.percent,
                    api_key=stripe.api_key
                )
                tax_rates.append(tax_rate.id)
            except Exception as e:
                print(f"Error creating tax rate: {e}")
        
        if tax_rates:
            for item in line_items:
                item['tax_rates'] = tax_rates

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                discounts=stripe_discounts,
                mode='payment',
                success_url=request.build_absolute_uri('/success'),
                cancel_url=request.build_absolute_uri('/cancel'),
            )
            return Response({'id': session.id})
        except Exception as e:
            print(f"Stripe Order Error: {e}") 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreatePaymentIntentView(APIView):
    def get(self, request, id):
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        stripe.api_key = get_stripe_api_key(item.currency)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=item.price,
                currency=item.currency,
                automatic_payment_methods={'enabled': True},
            )
            return Response({
                'clientSecret': intent.client_secret,
                'publicKey': get_stripe_keys(item.currency)[0] # Fixed usage
            })
        except Exception as e:
            print(f"Stripe Intent Error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
