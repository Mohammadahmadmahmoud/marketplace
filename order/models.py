from django.db import models

from product.models import Product
from core.models import *
from vendor.models import Vendor
from customer.models import Customer
from product.models import *

class Order(models.Model):
    customer = models.ForeignKey(Customer,  related_name='orders',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount= models.DecimalField(max_digits=8, decimal_places=2, null=True)
    vendors= models.ManyToManyField(Vendor, related_name='orders')
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE,null=True)
    ad = models.ForeignKey(Ads ,related_name='items', on_delete=models.CASCADE,null=True)
    s_part = models.ForeignKey(SilverPart,related_name='items', on_delete=models.CASCADE, null=True)
    f_part = models.ForeignKey(FreePart, related_name='items', on_delete= models.CASCADE, null=True )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    class Meta:
        ordering= ['-created_at']


    def __str__(self):
        return self.customer.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE, null=True)
    vendor_paid=models.BooleanField(default=False,null=True)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    quantity= models.IntegerField(default=1)


    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price*self.quantity
