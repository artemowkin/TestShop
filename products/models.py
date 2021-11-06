from uuid import uuid4

from django.db import models
from django.urls import reverse


class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField('category title', max_length=100, unique=True)

    class Meta:
        db_table = 'categories'
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField('product title', max_length=100)
    price = models.DecimalField(
        'product price', max_digits=15, decimal_places=2
    )
    short_description = models.CharField(
        'product short description', max_length=255
    )
    description = models.TextField('product description')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='product category'
    )
    pub_datetime = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'products'
        ordering = ('-pub_datetime', 'title')
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('concrete_product', args=[str(self.pk)])


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products')

    class Meta:
        db_table = 'product_images'

