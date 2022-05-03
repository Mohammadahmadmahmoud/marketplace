from django.contrib import admin
from .models import Product,Category


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display_link =    ['image','title',
                       'description','category',
                       'vendor',
                       'price','date_added',
                       
                       ]

admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductImage)
admin.site.register(Category)