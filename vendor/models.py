from django.db import models
from customer.models import User

class Vendor(models.Model):
 
    created_by = models.OneToOneField(User,related_name='vendor',on_delete=models.CASCADE, primary_key=True)
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=255, default='')
    address = models.CharField(max_length=100, default='')
    telephone = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ['name']


    def save(self, *args, **kwargs):
        super().save()
        
    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.created_by.id])
        return sum((item.product.final_price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.created_by.id])
        return sum((item.product.final_price * item.quantity) for item in items)
