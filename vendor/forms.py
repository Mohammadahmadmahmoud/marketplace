from django.forms import ModelForm
from product.models import Product,ProductImage
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import transaction
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields=['category','title','description','price']


class ProductImageForm(ModelForm):
    image = forms.ImageField(
        label="Image",
    widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )
    class Meta:
        model = ProductImage
        fields = ['image']


class RegisterForm(UserCreationForm):
    model = get_user_model()
    username = forms.CharField()
    email = forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vendor = True

        user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')

class EditFormVendor(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['first_name', 'last_name', 'email', 'address', 'telephone', 'zip_code', 'state']
