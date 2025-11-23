from rest_framework import serializers
from .models import Item, Order

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'currency']

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    discount = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'items', 'discount', 'tax']

    def get_discount(self, obj):
        return obj.discount.percent if obj.discount else None

    def get_tax(self, obj):
        return obj.tax.percent if obj.tax else None
