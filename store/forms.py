from django import forms
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm, 
UsernameField, PasswordResetForm, SetPasswordForm)
from .models import Profile, ShippingAddress

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Enter Password', widget = forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Again', widget = forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget= forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile', 'alternate_mobile', 'password1', 'password2']
        labels = {'email': 'Email Addrerss', 'mobile':'Mobile Number', 'alternate_mobile':'Alternate Mobile number'}
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'alternate_mobile': forms.TextInput(attrs={'class':'form-control'}),
             }

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode', 'country']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line_1' : forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.TextInput(attrs={'class':'form-control'}),
            'zipcode' : forms.NumberInput(attrs={'class':'form-control'}),
            'country' : forms.TextInput(attrs={'class':'form-control'}),
        }