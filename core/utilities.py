from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart
import vendor

from .models import Ads


def notify_vendor(ads):
    from_email = settings.DEFAULT_EMAIL_FROM

    for vendor in ads.vendors.all():
        to_email = vendor.created_by.email
        subject = 'Order confirmation'
        text_content = 'Thanks for the order!'
        html_content = render_to_string('core/email_notify_vendor.html', {'ads': ads, 'vendor': vendor})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(ads):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = ads.customer.email
    subject = 'Order confirmation'
    text_content = 'Thanks for the order!'
    html_content = render_to_string('core/email_notify_customer.html', {'ads': ads})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    
def checkout(request, customer):
    orderCustomer = Ads.objects.create(customer=customer)
  
    orderVendor = Ads.objects.create(vendor=vendor)

    return orderCustomer+' '+orderVendor
    
  
