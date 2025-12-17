from django.contrib import admin
from .models import Product, Garment, ArtPiece

# Register your models here.

admin.site.register(Product)
admin.site.register(Garment)
admin.site.register(ArtPiece)
