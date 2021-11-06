from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from products.models import Product


User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField(default=5, validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])
    text = models.CharField(max_length=500)
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        ordering = ('-pub_datetime',)

