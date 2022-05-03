from django import forms



class CheckoutForm(forms.Form):
    stripe_token=forms.CharField(max_length=255)
