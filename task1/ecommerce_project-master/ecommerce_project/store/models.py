# store/models.py
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    name       = models.CharField(max_length=300)
    slug       = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    image      = models.ImageField(upload_to='products/', blank=True, null=True)
    stock      = models.PositiveIntegerField(default=0)
    available  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                   default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shipping info
    full_name  = models.CharField(max_length=200)
    email      = models.EmailField()
    address    = models.TextField()
    city       = models.CharField(max_length=100)
    country    = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE,
                                  related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}× {self.product.name}"