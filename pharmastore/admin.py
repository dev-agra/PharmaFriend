from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGalllery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGalllery
    extra = 1

# Register your models here.
class VariationInline(admin.TabularInline):
    model = Variation #To get model as inline the said model must have foreign key to other model hence Variation
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'stock', 'category', 'exp_date', 'man_date', 'is_available', 'created_date', 'modified_date']
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline, VariationInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGalllery)


