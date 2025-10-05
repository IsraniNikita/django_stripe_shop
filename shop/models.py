from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price_cents = models.PositiveIntegerField(help_text="Price in cents")

    def price_display(self):
        return f"₹{self.price_cents / 100:.2f}"

    def __str__(self):
        return f"{self.name} - ₹{self.price_cents / 100:.2f}"


class Order(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_PAID = "PAID"
    STATUS_CHOICES = [(STATUS_PENDING, "Pending"), (STATUS_PAID, "Paid")]

   # in shop/models.py
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def total_cents(self):
        return sum(item.line_total_cents() for item in self.items.all())

    def total_display(self):
        return f"₹{self.total_cents() / 100:.2f}"

    def __str__(self):
        return f"Order {self.id} - {self.status} ({self.user.username})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_cents = models.PositiveIntegerField(help_text="Snapshot of product price in cents")

    def line_total_cents(self):
        return self.price_cents * self.quantity

    def line_total_display(self):
        return f"₹{self.line_total_cents() / 100:.2f}"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
