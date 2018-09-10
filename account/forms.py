from django import forms
from django.forms import DateTimeField
from account.models import Employee
from django.db import models
from datetime import datetime#

class SignupForm(forms.Form):

    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Joe', 'size': 40, 'class': 'form-control'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Doe', 'size': 40, 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'name@clumsy.com', 'size': 40, 'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '123 Street, San Diego, CA 92122', 'size': 40, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'size': 40, 'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '(800) 123-4567', 'size': 40, 'class': 'form-control'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Clumsy Employee', 'size': 40, 'class': 'form-control'}))
    profilePic = forms.ImageField(required=False)
    
class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'name@example.com', 'size': 40, 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'size': 40, 'class': 'form-control'}))
    
class PostForm(forms.Form):
    when = datetime.now
    post= forms. CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 12}))
    

class CommentForm(forms.Form):
    when = datetime.now
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 12}))
