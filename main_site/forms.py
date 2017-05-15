from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
class AuthForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    
class BlogPostForm_Web(forms.ModelForm): #Для сайта
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
    
class BlogPostForm(forms.ModelForm): #Для админки
    class Meta:
        model = BlogPost
        fields = ['author','title','text', 'date_published', 'already_sent', 'order_to_sent']
        
