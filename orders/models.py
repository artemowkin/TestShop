from django.db import models
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator
)
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import Product


User = get_user_model()


class Receiver(models.Model):
    """Model of order receiver"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
        ),
    ], unique=True)

    class Meta:
        db_table = 'receivers'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class Address(models.Model):
    """Model of order address"""
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=5)
    apartment = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=6)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return (
            f"{self.city}, {self.street}, {self.house}, {self.apartment}, "
            f"({self.postal_code})"
        )


class Order(models.Model):
    """Orders model"""
    products = models.ManyToManyField(Product, related_name='orders')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(max_length=10, choices=(
        ('processing', 'processing'),
        ('received', 'received'),
        ('sent', 'sent'),
        ('closed', 'closed')
    ), default='processing')
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'
        ordering = ('-pub_datetime',)

    def get_absolute_url(self) -> str:
        return reverse('concrete_order', args=[self.pk])
