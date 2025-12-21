from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    """
    Model representing an e-commerce product.
    We will search across name, description, and SKU.
    """
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default="men")
    description = models.TextField()
    size = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU/Product Code")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    produt = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')
    
    def __str__(self):
        return f"Image for {self.produt.name}"
    
class cartItem(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=40, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (x{self.quantity}) - M{self.price * self.quantity}"
    
    def total_price(self):
        return self.price * self.quantity
    
class Garment(models.Model):
    """Garments to be chosen for drawing"""
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default="men")
    fabric = models.CharField(max_length=100, default="ANCanva")
    size = models.CharField(max_length=50)
    price =models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='garments/', null=True , blank=True)
    
    def __str__(self):
        return self.name
    
class ArtPiece(models.Model):
    """Art to be chosen for drawing"""
    
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=100, default="ANCanvas")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='arts/')
    
    def __str__(self):
        return self.title
    
class customItem(models.Model):
    """Fully customized item to be put to cart"""
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default="men")
    size = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU/Product Code")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='custom_Items/', null=True, blank=True)
    fabric = models.CharField(max_length=100, default="ANCanva")
    artist = models.CharField(max_length=100, default="ANCanvas")

    def __str__(self):
        return self.name
    
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    guest_session_key = request.session.session_key
    
    cartItem.objects.filter(session_id=guest_session_key).update(user=user, session_id=None)
    
    