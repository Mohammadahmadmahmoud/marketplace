from django.urls import path

from . import views
from customer import views as customer_views
from vendor import views as vendor_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('customer-card', views.cart_detail, name='cart'),
    path('vendor-cart/', views.vendor_cart, name='vendor_cart'),
    
    path('success/', views.success, name='success'),
    path('problem/', views.problem, name='problem'),
    path('customer-login/',customer_views.LoginView.as_view(),name='customer_login'),
    path('vendor-login/',vendor_views.LoginView.as_view(),name='vendor'),
]
