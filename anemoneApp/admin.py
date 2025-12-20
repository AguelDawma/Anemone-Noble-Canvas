from django.contrib import admin
from .models import Product, Garment, ArtPiece, ProductImage

# Register your models here.

admin.site.register(Garment)
admin.site.register(ArtPiece)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    
@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
