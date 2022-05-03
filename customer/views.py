from re import A
from webbrowser import get
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from cart.views import success
from core.utilities import checkout, notify_customer, notify_vendor
from django.views import generic
from core.models import *
from .models import Customer, SecurityQuestion
from django.contrib.auth import views as auth_views
from django.contrib import auth
from django.views import View
from .forms import RegisterForm, EditForm, InformationControlForm, PasswordUpdateForm,LoginForm
from .models import User
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from core.decorators import user_password, unauthenticated_user, allowed_users, admin_only, customer_required
from django.contrib import messages
from core.forms import AdsForm
from django.utils.text import slugify
from django.conf import settings
import stripe
from order.utilities import checkout
from cart.forms import CheckoutForm
from django.urls import reverse_lazy
 
 
 
# class RegisterView(generic.CreateView):
#     form_class = RegisterForm
#     template_name = 'customer/register.html'
#     success_url = reverse_lazy('home')
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_customer')

    else:
        form = RegisterForm()
    return render(request, 'customer/register.html', {'form': form})

@login_required
@customer_required
def add_ads(request):
    if request.method =='POST':
        form =AdsForm(request.POST, request.FILES)

        if form.is_valid():
            ads = form.save(commit=False)
            ads.customer=request.user.customer
            ads.slug = slugify(ads.title)
            ads.save()

            return redirect('pack_confirm')
    else:
        form = AdsForm()

    return render(request, 'customer/add_ads.html',{'form':form})
def pack_confirm(request):
    add_pack = SilverPart.objects.all()
    free_pack = FreePart.objects.all()

    return render(request, 'core/pack_confirm.html', {'add_pack':add_pack,'free_pack':free_pack})
@login_required
def ads_checkout(request):
    customer=Customer.objects.get(user_id=request.user.id)
    # item=SilverPart.objects.filter(customer=customer).first()
    
    # if item:price=item.get_price()
    # else:price=5.00
    price=100
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
                        description='AU79 Code market place Price',
                        source=stripe_token
                        )
                    order = checkout(request,customer, final_price)
                    # notify_customer(order)
         

                    return redirect('success')
                except Exception as e:
                    print(e)
                    return redirect('problem')
                    messages.error(request,'Your order could not be created')
        else:
            form = CheckoutForm()
    return render(
                   request,
                   'customer/ads_checkout.html',{
                    'customer':customer,
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'vat_amount':vat_amount,
                    'price':price,
                    'vat':vat,
                    'final_price':final_price
                    })


@login_required
def gold_ads_checkout(request):
    customer=Customer.objects.get(user_id=request.user.id)
    # item=SilverPart.objects.filter(customer=customer).last()
    
    # if item:price=item.get_price()
    # else:price

    
    # if item:price=item.get_price()
    # else:price=100
    price=100
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
                        amount= int(price*100),
                        
                        currency='AED',
                        description='how is Code market place Price',
                        source=stripe_token
                        )
         
                    
                    return redirect('success')     
                except Exception as e:
                
                    print(e)
    return render(
                   request,
                   'customer/ads_checkout.html',{
                    'customer':customer,
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'price':price,
                    'vat':vat,
                    'vat_amount':vat_amount,
                    'final_price':final_price
               
                    })

@login_required
def silver_ads_checkout(request):
    customer=Customer.objects.get(user_id=request.user.id)
    # item=SilverPart.objects.filter(customer=customer).first()
    
    # if item:price=item.get_price()
    # else:price=50
    price=100
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
                    order = checkout(request,customer, final_price)

                    return redirect('success')     
                except Exception as e:
                
                    print(e)
                    return redirect('problem')
                    messages.error(request,'Your order could not be created')
                
        else:
            form = CheckoutForm()
    return render(
                   request,
                   'customer/ads_checkout.html',{
                    'customer':customer,                 
                    'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY,
                    'vat_amount':vat_amount,
                    'price':price,
                    'vat':vat,
                    'final_price':final_price
                    })



@login_required
@customer_required
def customer_profile(request):
    ads = Ads.objects.all()
    customer = request.user.customer
    orders = customer.orders.all()
    ads_order = customer.ads.all()
    return render(request, 'customer/customer_profile.html', {'ads_order':ads_order,'customer': customer, 'orders': orders})


def customers(request):
    customers = Customer.objects.all()
    return render(request, 'customer/customers.html', {'customers': customers})


class LogoutView(auth_views.LogoutView):
    template_name = 'customer/customer_profile.html'

    def get_success_url(self):
        return resolve_url('home')
    


class LoginView(auth_views.LoginView):
    def get(self, request):
        return render(request, 'customer/customer_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_customer:
                    auth.login(request, user)
                    return redirect('customer_profile')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'customer/customer_login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'customer/customer_login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'customer/customer_login.html')


@login_required
def edit_customer(request):
    customer = Customer.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = EditForm(data=request.POST,instance=customer)

        if form.is_valid():
            form.save()
            return redirect('customer_profile')

    else:
        form = EditForm(instance=customer)
    return render(request, 'customer/edit_customer.html', {'form': form})


def orders(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = customer.orders.all()
    return render(request, 'customer/orders.html', {'customer': customer, 'orders': orders})


def customer_control(request):
    form = InformationControlForm()
    if request.method == 'POST':
        username = request.POST['username']
        security_question_id = request.POST['security_question']
        security_question_answer = request.POST['security_question_answer']

        security_question = get_object_or_404(SecurityQuestion, pk=security_question_id)

        customer = Customer.objects.get(user__username=username)
        user = User.objects.get(username=username)
        if customer.check_security_question_answer(security_question_answer) & customer.check_security_question(
                security_question):
            if user.is_customer:
                auth.login(request, user)
                return redirect('password_update')

        else:
            return redirect('frontpage')

    return render(request, 'customer/customer_control.html', {'form': form})

def password_update(request):

    form = PasswordUpdateForm()
    if request.method == 'POST':
        try:
            username = request.POST['username']
            user = User.objects.get(username=username)
            password = request.POST['password1']
            user.set_password(password)
            user.save()
        
            return redirect('password_success')
        except:
            return redirect('problem')
            

    else:
        form = PasswordUpdateForm()
    return render(request, 'customer/password_update.html', {'form': form})


def password_success(request):
    return render(request, 'customer/customer_password_success.html')



@customer_required
def update(request,pk):
    
    
    ads = Ads.objects.get(id=pk)
    form = AdsForm(instance=ads)

    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES, instance=ads)
        if form.is_valid():
            form.save()
            return redirect('ads_page')

    context = {
        "form":form
    }

    return render(request, 'customer/update.html', context)

# Delete Product
@customer_required
def delete(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.delete()
    return redirect('ads_page')
