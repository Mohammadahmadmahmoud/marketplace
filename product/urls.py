from django.urls import path

from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings

urlpatterns= [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<int:product_slug>/', views.product, name='product'),
    # path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.category, name='category'),
]

