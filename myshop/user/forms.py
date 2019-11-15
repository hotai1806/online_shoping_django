from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea)
    name_profile = forms.CharField(required=False)
    numberphone = forms.CharField(required=False)

class AccountForm(forms.Form):
    name_profile = forms.CharField(required=False)
    numberphone = forms.CharField(required=False)
    shipping_address = forms.CharField(widget=forms.Textarea)


class PaymentForm(forms.Form):
    use_default = forms.BooleanField(required=False)
