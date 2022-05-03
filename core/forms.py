from django.forms import ModelForm
from product.models import Product
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django.contrib.auth.models import Group


class AdsForm(ModelForm):
    image = forms.ImageField(
        label="Image",
    widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
    class Meta:
        model=Ads
        fields=['name','category','image','title','description','video','url']


class CheckoutForm(forms.Form):
    stripe_token=forms.CharField(max_length=255)
