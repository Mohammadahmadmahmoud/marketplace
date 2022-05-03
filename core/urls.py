from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('', views.frontpage, name='frontpage'),
    path('ads_page/', views.ads_page, name='ads_page'),
    path('ads/',views.ads, name='ads'),
    path('<slug:category_ads_slug>/<int:ads_slug>/', views.category, name='ads'),
    path('<slug:category_slug>/', views.category, name='category'),
    # path('contact/', views.contact, name ='contact'),
]
