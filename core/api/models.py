from django.db import models

class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g. 10.5 for 10.5%)")

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tax percentage (e.g. 20.0 for 20%)")

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(help_text="Price in cents/smallest unit") 
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency})"

class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"
    
    def get_total_price(self):
        total = sum(item.price for item in self.items.all())
        
        # Apply discount if exists
        if self.discount:
            total = total * (1 - self.discount.percent / 100)
            
        # Apply tax if exists
        if self.tax:
            total = total * (1 + self.tax.percent / 100)
            
        return int(total)
