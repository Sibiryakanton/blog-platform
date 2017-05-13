from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django import forms

from django.utils import timezone
import datetime

from django.contrib.auth import authenticate, login, logout

def index(request): #Главная страница, она же фид-лента (если пользователь анонимен, отображается форма входа)
	if request.user in User.objects.all():
		template_name='index-feed.html'
		title = 'Фид-лента'
		blog_user_info = PersonalBlog.objects.get(author=request.user) #Информация о читателе
		noted_list = blog_user_info.noted.all()
		feed_list = blog_user_info.feeds.all()
		post_list = BlogPost.objects.filter(author__in=feed_list).order_by('-date_published')
		context = { 'title':title, 'post_list':post_list, 'noted_list':noted_list}
	else: #Если пользователь авторизован, показываем ленту, иначе отправляем на форму входа
		template_name='login.html'
		title = 'Форма входа'
		form = AuthForm()
		context = {'form':form, 'title':title}
	return render(request, template_name, context)

	
def blog_page(request, username): #Страница блога
	template_name = 'blog.html'
	blog_author = User.objects.get(username=username) #Имя автора, на блог которого переходит пользователь
	title='Блог пользователя {}'.format(blog_author.username)
	blog_posts = BlogPost.objects.filter(author=blog_author).order_by('-date_published')
	reader_info = PersonalBlog.objects.get(author = request.user) #Запрашиваем данные о пользователе, 
						#чтобы в шаблоне подставлять "Вы уже подписаны" вместо "Подписаться" при необходимости
	
	check_feed_exist=False
	if blog_author in reader_info.feeds.all():
		check_feed_exist=True
	
	context = {'blog_posts':blog_posts, 'check_feed_exist':check_feed_exist, 'title':title,'blog_author':blog_author.username}
	return render(request, template_name, context )
	

def add_post(request): # Страница формы добавления поста
	template_name='add_post.html'
	title_web='Форма создания поста'
	context={}
	if request.method=='POST':
		form = BlogPostForm_Web(request.POST)
		author = request.user
		title = request.POST.get('title','')
		slug = request.POST.get('slug','')
		text = request.POST.get('text','')
		order_to_sent = True
		already_sent = False
		date_published = timezone.now()
		
		post = BlogPost(author=author,title=title,slug=slug, text=text, order_to_sent=order_to_sent,already_sent=already_sent,date_published=date_published)
		post.save()
		return redirect('/')
	else:
		form = BlogPostForm_Web
		context={'form':form, 'title':title_web}
		return render(request, template_name, context)

def subscribe(request, username): #Обработчик подписки с редиректом на главную
	blog_owner = User.objects.get(username=username)
	blog = PersonalBlog.objects.get(author=blog_owner) #Карточка пользователя-автора
	self_user_info = PersonalBlog.objects.get(author=request.user) #Карточка пользователя-читателя
	self_user_info.feeds.add(blog.author)
	blog.followers.add(self_user_info.author)
	return redirect('/')

def unsubscribe(request, username): #Обработчик подписки с редиректом на главную
	blog_owner = User.objects.get(username=username)
	blog = PersonalBlog.objects.get(author=blog_owner)
	self_user_info = PersonalBlog.objects.get(author=request.user)
	self_user_info.feeds.remove(blog.author)
	blog.followers.remove(self_user_info.author)
	return redirect('/')
	
def note(request, post_id): #Обрабтчик клика на кнопку "Уже прочитано"
	current_post = BlogPost.objects.get(pk=post_id)
	reader_info = PersonalBlog.objects.get(author = request.user)
	reader_info.noted.add(current_post)
	return redirect('/')
	

def send_mail(request):
	mail_host = EMAIL_HOST_USERSMTP+"@gmail.com" 
	user_list = User.objects.all()
	recipients= []
	for user in user_list:
		if user.email=='':
			continue
		else:
			recipients.append(user.email)
	message = '''
		В блоге из ваших подписок появилась новая запись!'''
	subject= 'Новый пост'
	send_mail(subject, message, mail_host.mail, recipients, fail_silently=False)
	return redirect('/')