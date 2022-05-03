from django.contrib import admin
from .models import OrderItem,Order

# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','vendor','price','quantity','get_total_price']


 
admin.site.register(OrderItem,OrderItemAdmin) 