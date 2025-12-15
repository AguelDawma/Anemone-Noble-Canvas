from django.db import models

# Create your models here.
class cartItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} (x{self.quantity}) - ${self.price * self.quantity}"
    
    def total_price(self):
        return self.price * self.quantity

class Product(models.Model):
    """
    Model representing an e-commerce product.
    We will search across name, description, and SKU.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU/Product Code")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name