from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor
from django.utils.text import slugify
from product.models import Product,ProductImage
from .forms import ProductForm, RegisterForm,EditFormVendor,ProductImageForm,LoginForm
from .models import User
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
from core.decorators import unauthenticated_user,allowed_users,vendor_required
from django.contrib import messages
from django.contrib import auth
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from core.utilities import checkout, notify_customer, notify_vendor
from weasyprint import HTML
import stripe
import mimetypes
import os
from django.conf import settings
from core.forms import *
from core.models import *
from django.urls import reverse_lazy
from django.views import generic
# Sign Up As Vendor

# class RegisterView(generic.CreateView):
#     form_class = RegisterForm
#     template_name = 'vendor/become_vendor.html'
    # success_url = reverse_lazy('vendor_login')
def become_vendor(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)

            vendor=Vendor.objects.create(name=user.username, created_by=user)

            return redirect('edit_vendor')

    else:
        form =RegisterForm()
    return render(request,'vendor/become_vendor.html', {'form':form})
    

@vendor_required
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    success_url = reverse_lazy()
    template_name = 'vendor/vendor_login.html'


# Vendor Product Deatail
@login_required
@vendor_required
def vendor_admin(request):
    
    vendor = request.user.vendor
    products =vendor.products.all()
    orders = vendor.orders.all()
    ads_order = vendor.ads.all()

    for order in orders:
        order.vendor_amount=0
        order.vendor_paid_amount=0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor==request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()

                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False


    return render(request,'vendor/vendor_admin.html',{'ads_order':ads_order,'vendor':vendor,'products':products, 'orders':orders})

# Venor Addig Products
@login_required
def add_product(request):
    if request.method =='POST':
        form =ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor=request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()
    return render(request, 'vendor/add_product.html',{'form':form})

# Update Product
@vendor_required
def updateProduct(request,pk):
    
    vendor = request.user.vendor
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    image_form = ProductImageForm(request.POST, request.FILES)

    if request.method == 'POST':
        # form = ProductForm(request.POST, request.FILES, instance=product)
        # image_form = ProductImageForm(request.POST, request.FILES)
        
        if image_form.is_valid():
            productimage = image_form.save(commit=False)
            productimage.product = product
            productimage.save()
            return redirect('vendor_admin')
        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
        
        # if form.is_valid():
        #     form.save()
        #     return redirect('vendor_admin')

    context = {
        "form":form,
        'image_form':image_form,
        'product':product
    }

    return render(request, 'vendor/updateProduct.html', context)

# Delete Product
@vendor_required
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('vendor_admin')




# Adding Ads For Vendor

 
 
def vendor_add_ads(request):
    if request.method =='POST':
        form =AdsForm(request.POST, request.FILES)

        if form.is_valid():
            ads = form.save(commit=False)
            ads.vendor=request.user.vendor
            ads.slug = slugify(ads.title)
            ads.save()

            return redirect('pack_confirm')
    else:
        form = AdsForm()

    return render(request, 'vendor/vendor_add_ads.html',{'form':form})

# Update Ad

 
def update_vendor_ads(request,pk):
    
    ads = Ads.objects.get(id=pk)
    form = AdsForm(instance=ads)

    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES, instance=ads)
        if form.is_valid():
            form.save()
            return redirect('vendor_admin')

    context = {
        "form":form
    }

    return render(request, 'vendor/update_vendor_ads.html', context)

# Delete Ad
@vendor_required
def delete_vendor_ads(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.delete()
    return redirect('vendor_admin')


# Vendor Edite Profile
@login_required
@vendor_required
def edit_vendor(request):
    
    vendor = request.user.vendor

    form = EditFormVendor(request.POST or None)
    
    if request.method == 'POST':
        form = EditFormVendor(data=request.POST,instance=vendor)


        if form.is_valid():
            form.save()
            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html',{'vendor':vendor,'form':form})


# Vendors List
def vendors(request):
    vendors= Vendor.objects.all()
    return render(request, 'vendor/vendors.html',{'vendors':vendors})


def vendor(request, vendor_id):
    vendor=get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'vendor/vendor.html',{'vendor':vendor})



# Normal Pack
@vendor_required
@login_required
def vendor_ads_checkout(request):
    user=User.objects.get(pk=request.user.pk)
    item=SilverPart.objects.filter(user=user).first()
    
    if item:price=item.get_price()
    else:price=5.00
    vat = 0.05
    vat_amount = price*vat
    final_price = price+vat_amount
    form = CheckoutForm(request.POST)
    if request.method=='POST':
        print(form.is_valid())
        if form.is_valid():
            stripe.api_key= settings.STRIPE_SECRET_KEY
            stripe_token=form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                    amount= int(final_price*100),
                    
                    currency='AED',
                    description='how is Code market place Price',
                    source=stripe_token
                    )


                return redirect('success')
            except Exception as e:
                print(e)
                return redirect('problem')
                messages.error(request,'Your order could not be created')
        else:
            form = CheckoutForm()
    return render(
                   request,
                   'vendor/vendor_ads_checkout.html',{
                    'user':user,
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'vat_amount':vat_amount,
                    'price':price,
                    'vat':vat,
                    'final_price':final_price
                    })
# Golden Pack
@vendor_required
@login_required
def vendor_gold_ads_checkout(request):
    user=User.objects.get(pk=request.user.pk)
    item=SilverPart.objects.filter(user=user).first()
    
    if item:price=item.get_price()
    else:price=100
    vat = 0.05
    vat_amount = price*vat
    final_price = price+vat_amount
    form = CheckoutForm(request.POST)
    if request.method=='POST':
        print(form.is_valid())
        if form.is_valid():
                stripe.api_key= settings.STRIPE_SECRET_KEY
                stripe_token=form.cleaned_data['stripe_token']
                try:
                    charge = stripe.Charge.create(
                        amount= int(final_price*100),
                        
                        currency='AED',
                        description='how is Code market place Price',
                        source=stripe_token
                        )


           
                    return redirect('success')
                except Exception as e:
                    print(e)
                    return redirect('problem')
                messages.error(request,'Your order could not be created')
        else:
            form = CheckoutForm()
    return render(
                   request,
                   'vendor/vendor_ads_checkout.html',{
                    'user':user,
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'vat_amount':vat_amount,
                    'price':price,
                    'vat':vat,
                    'final_price':final_price
                    })
    
# Silver Pack
@vendor_required
@login_required
def vendor_silver_ads_checkout(request):
    user=User.objects.get(pk=request.user.pk)
    item=SilverPart.objects.filter(user=user).first()
 
    if item:price=item.get_price()
    else:price=50
    vat = 0.05
    vat_amount = price*vat
    final_price = price+vat_amount
    form = CheckoutForm(request.POST)
    if request.method=='POST':
        print(form.is_valid())
        if form.is_valid():
                stripe.api_key= settings.STRIPE_SECRET_KEY
                stripe_token=form.cleaned_data['stripe_token']
                try:
                    charge = stripe.Charge.create(
                        amount= int(final_price*100),
                        
                        currency='AED',
                        description='how is Code market place Price',
                        source=stripe_token
                        )


           
                    return redirect('success')
                except Exception as e:
                    print(e)
                    return redirect('problem')
                messages.error(request,'Your order could not be created')
        else:
            form = CheckoutForm()
    return render(
                   request,
                   'vendor/vendor_ads_checkout.html',{
                    'user':user,
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'vat_amount':vat_amount,
                    'price':price,
                    'vat':vat,     
                    'final_price':final_price
                    })



class LogoutView(auth_views.LogoutView):
    template_name = 'vendor/vendor_admin.html'
    def get_success_url(self):
        return resolve_url('frontpage')



class LoginView(View):
    def get(self, request):
        return render(request, 'vendor/vendor_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_vendor:
                    auth.login(request, user)

                    return redirect('vendor_admin')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'vendor/vendor_login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'vendor/vendor_login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'vendor/vendor_login.html')


def html_to_pdf_view(request):
    vendor = request.user.vendor
    products =vendor.products.all()
    orders = vendor.orders.all()
    for order in orders:
        order.vendor_amount=0
        order.vendor_paid_amount=0
        order.fully_paid = True

        for item in order.items.all():

            if item.vendor==request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()

                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    html_string = render_to_string('vendor/pdf_template.html',{'vendor':vendor,'products':products, 'orders':orders})

    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/orders.pdf');

    fs = FileSystemStorage('/tmp')
    with fs.open('orders.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
        return response

    return response

