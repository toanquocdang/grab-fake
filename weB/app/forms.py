from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm,SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer, Product, Merchants, Rider
from django.forms import ModelForm

class CustomerLogin(AuthenticationForm):
    username= UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

ROLE_CHOICES = (
        ('Customer', 'Customer'),
        ('Rider', 'Rider'),
        ('Merchants', 'Merchants'),
    )
class CutomerSingup(UserCreationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields  = ['username', 'email', 'password1','password2','role']

class CutomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','email','address','city','state','phone']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
        }
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ( 'merchants','name', 'price', 'digital','address','image')
        labels = {
            'name': '',
            'price': '',
            'address': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Produst name'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Price'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address'}),
         }

class MerchantsProfileForm(forms.ModelForm):
    class Meta:
        model = Merchants
        fields = ['name','email','phone','address_rd']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
            'address_rd': forms.TextInput(attrs={'class':'form-control'}),
        }


class RiderProfileForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = ['name', 'email', 'xe', 'phone', 'address_rd', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'xe': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'address_rd': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpdatePriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price']

