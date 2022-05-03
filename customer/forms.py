from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    model = get_user_model()
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput )
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user, first_name=self.cleaned_data.get('first_name'),
                                           last_name=self.cleaned_data.get('last_name'),
                                           email=self.cleaned_data.get('email'))
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email /UserName')

class EditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'address', 'telephone', 'zip_code', 'state', 'security_question',
                  'security_question_answer']


class InformationControlForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ['username', 'email', 'security_question', 'security_question_answer']


class PasswordUpdateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')
