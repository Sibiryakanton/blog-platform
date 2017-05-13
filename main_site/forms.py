from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
class AuthForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)
	
class BlogPostForm_Web(forms.Form): #Для сайта
	author = forms.CharField(widget=forms.HiddenInput())
	title=forms.CharField()
	slug=forms.SlugField()
	text=forms.CharField(widget=forms.Textarea())
	date_published=forms.DateTimeField(widget=forms.HiddenInput(attrs={'type':'date'}))

class BlogPostForm(forms.ModelForm): #Для админки
	class Meta:
		model = BlogPost
		fields = ['author','title', 'slug', 'text', 'date_published', 'already_sent', 'order_to_sent']
		
