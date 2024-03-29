from django import forms
from django.forms import DateTimeField
from account.models import Employee
from django.db import models
from datetime import datetime
from tinymce.widgets import TinyMCE

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
    CHOICES = [
        ('Anonymous', 'Anonymous'),
        ('NotAnonymous', 'As me')
    ]

    anonymity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject', 'size': 40, 'class': 'form-control'}))
    post = forms.CharField(widget=TinyMCE(attrs={'cols': 181, 'rows': 15}))

class UpdateForm(forms.Form):
    STATUS = [
        ('Resolved', 'Resolved'),
        ('Unresolved', 'Unresolved')
    ]
    status = forms.ChoiceField(choices=STATUS, widget=forms.RadioSelect())

class VisibilityForm(forms.Form):
    VISIBILITY = [
        ('Not Seen', 'Not Seen'),
        ('Seen', 'Seen')
    ]
    visibility = forms.ChoiceField(choices=VISIBILITY, widget=forms.RadioSelect())

class EditProfileForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '(800) 123-4567', 'size': 40, 'class': 'form-control'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Clumsy Employee', 'size': 40, 'class': 'form-control'}))
    profilePic = forms.ImageField(required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '123 Street, San Diego, CA 92122', 'size': 40, 'class': 'form-control'}))

class CommentForm(forms.Form):
    CHOICES = [
        ('Anonymous', 'Anonymous'),
        ('NotAnonymous', 'As me')
    ]

    anonymity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    comment = forms.CharField(widget=TinyMCE(attrs={'cols': 181, 'rows': 15}))
