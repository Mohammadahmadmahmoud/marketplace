from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from core.models import *
from product.models import Product
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from cart.cart import Cart
from .forms import AdsForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator
import random
import mimetypes
 

def frontpage(request):
    newest_products=Product.objects.all()
    pagina = Paginator(newest_products,2)
    page = request.GET.get('page')
    prod = pagina.get_page(page)
    

    return render(request,'core/frontpage.html',{'newest_products':newest_products,'prod':prod} )
 
# View Function For Ads Page .
def ads_page(request):
    newest_ads =   Ads.objects.filter(approved='True').all()
    adsPagina = Paginator(newest_ads,2)
    page = request.GET.get('page')
    ads = adsPagina.get_page(page)
    return render(request,'core/ads_page.html',{'newest_ads':newest_ads,'ads':ads})

def ads(request, category_slug, ads_slug):
 

    ads = get_object_or_404(Ads, category__slug=category_slug, id=ads_slug)

    

    similar_products = list(ads.category.ads.exclude(id=ads.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    return render(request, 'core/ads.html',
                  { 'ads': ads, 'similar_products': similar_products})


def category(request, category_slug):
    category = get_object_or_404(CategoryAds, slug=category_slug)

    return render(request, 'core/category.html', {'category': category})


# View Function For Contact Page .

# def contact(request):
#     return render(request,'core/contact.html')

# def category_ads(request, category_slug):
#     categoryads = get_object_or_404(CategoryAds, slug=category_slug)

#     return render(request, 'product/category.html', {'categoryads': categoryads})
