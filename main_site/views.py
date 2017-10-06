from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.models import User

from django.conf import settings

from .models import *
from .forms import *
from django import forms

from django.utils import timezone
import datetime
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .note import FeedManager


class index(TemplateView):  # Главная страница, она же фид-лента (если пользователь анонимен, отображается форма входа)
    def get(self, request, ordering='AZ', *args, **kwargs):
        if request.user in User.objects.all():
            template_name = 'index-feed.html'
            title = 'Фид-лента'
            blog_user_info = PersonalBlog.objects.get(author=request.user)  # Информация о читателе
            noted_list = blog_user_info.noted.all()
            feed_list = blog_user_info.feeds.all()
            post_list = BlogPost.objects.order_by('-date_published')
            context = {'title': title, 'post_list': post_list, 'noted_list': noted_list, 'ordering': ordering}

        else:  # Если пользователь авторизован, показываем ленту, иначе отправляем на форму входа
            template_name = 'login.html'
            title = 'Форма входа'
            form = AuthForm()
            context = {'form': form, 'title': title}
        return render(request, template_name, context)


class index2(TemplateView):  # Главная страница, она же фид-лента (если пользователь анонимен, отображается форма входа)
    def get(self, request, *args, **kwargs):
        if request.user in User.objects.all():
            template_name = 'index-feed.html'
            title = 'Фид-лента'
            blog_user_info = PersonalBlog.objects.get(author=request.user)  # Информация о читателе
            noted_list = blog_user_info.noted.all()
            feed_list = blog_user_info.feeds.all()
            post_list = BlogPost.objects.order_by('-date_published')
            context = {'title': title, 'post_list': post_list, 'noted_list': noted_list}
        else:  # Если пользователь авторизован, показываем ленту, иначе отправляем на форму входа
            template_name = 'login.html'
            title = 'Форма входа'
            form = AuthForm()
            context = {'form': form, 'title': title}
        return render(request, template_name, context)


class blog_page(TemplateView):
    def get(self, request, username):  # Страница блога
        template_name = 'blog.html'
        blog_author = User.objects.get(username=username)  # Имя автора, на блог которого переходит пользователь
        title = 'Блог пользователя {}'.format(blog_author.username)
        blog_posts = BlogPost.objects.filter(author=blog_author).order_by('-date_published')
        reader_info = PersonalBlog.objects.get(author=request.user)  # Запрашиваем данные о пользователе,
        # чтобы в шаблоне подставлять "Вы уже подписаны" вместо "Подписаться" при необходимости

        check_feed_exist = False
        if blog_author in reader_info.feeds.all():  # Проверяем, есть ли автор в подписках
            check_feed_exist = True

        context = {'blog_posts': blog_posts, 'check_feed_exist': check_feed_exist, 'title': title, 'blog_author': blog_author.username}
        return render(request, template_name, context)


class post_page(TemplateView):
    def get(self, request, post_pk, username):
        template_name = 'post.html'
        current_post = BlogPost.objects.get(pk=post_pk)

        title_web = 'Запись от пользователя {}'.format(username)
        blog_author = User.objects.get(username=username)
        reader_info = PersonalBlog.objects.get(author=request.user)  # Запрашиваем данные о пользователе,
        # чтобы в шаблоне подставлять "Вы уже подписаны" вместо "Подписаться" при необходимости
        check_feed_exist = False
        if blog_author in reader_info.feeds.all():  # Проверяем, есть ли автор в подписках
            check_feed_exist = True

        context = {'post': current_post, 'title': title_web, 'blog_author': blog_author.username, 'check_feed_exist': check_feed_exist}
        return render(request, template_name, context)


class add_post(FormView):  # Страница формы добавления поста
    def post(self, request):
        template_name = 'add_post.html'
        title_web = 'Форма создания поста'
        form = BlogPostForm_Web(request.POST)
        author = request.user
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        order_to_sent = True
        already_sent = False
        date_published = timezone.now()

        post = BlogPost(author=author, title=title, text=text, order_to_sent=order_to_sent, already_sent=already_sent, date_published=date_published)
        post.save()

        current_blog = PersonalBlog.objects.get(author=post.author)
        current_blog.posts.add(BlogPost.objects.get(pk=post.pk))
        if post.order_to_sent:
            mail_host = "oriflamesender@gmail.com"
            user_list = User.objects.all()
            recipients = []
            for user in user_list:
                if user.email == '' or user.email == post.author.email:
                    continue
                else:
                    recipients.append(user.email)
            message = 'У пользователя {0} в блоге появилась новая запись!Ссылка:{1}'.format(post.author, 'http://' + request.get_host() + post.get_absolute_url())
            subject = 'Новый пост'
            send_mail(subject, message, mail_host, recipients, fail_silently=False)
            post.order_to_sent = False  # Двойная проверка нужна на случай,если пользователь захочет оповестить несколько раз
            post.already_sent = True
            post.save()
        return redirect('/')

    def get(self, request):
        template_name = 'add_post.html'
        title_web = 'Форма создания поста'
        form = BlogPostForm_Web
        context = {'form': form, 'title': title_web}
        return render(request, template_name, context)


class edit_post(FormView):
    def post(self, request, post_pk, username):
        post = BlogPost.objects.get(pk=post_pk)
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_page', post_pk=post_pk, username=username)

    def get(self, request, post_pk, username):
        post = BlogPost.objects.get(pk=post_pk)
        form = BlogPostForm_Web(instance=post)
        return render(request, 'add_post.html', {'form': form})


class subscribe(View):
    def get(self, request, user_name):  # Обработчик подписки с редиректом на главную
        blog_owner = User.objects.get(username=user_name)
        blog = PersonalBlog.objects.get(author=blog_owner)  # Карточка пользователя-автора
        self_user_info = PersonalBlog.objects.get(author=request.user)  # Карточка пользователя-читателя
        self_user_info.feeds.add(blog.author)
        blog.followers.add(self_user_info.author)
        return redirect('/')


class unsubscribe(View):
    def get(self, request, user_name):  # Обработчик подписки с редиректом на главную
        blog_owner = User.objects.get(username=user_name)
        blog = PersonalBlog.objects.get(author=blog_owner)
        self_user_info = PersonalBlog.objects.get(author=request.user)
        noted_posts_of_author = self_user_info.noted.filter(author=blog_owner)  # Поиск в M2M-поле посты
        # автора блога, от которого отписывается пользователь

        for noted_element in noted_posts_of_author:
            self_user_info.noted.remove(noted_element)  # Попытка удаления

        self_user_info.feeds.remove(blog.author)
        blog.followers.remove(self_user_info.author)
        self_user_info.save()
        '''manager = FeedManager(request)
        manager.remove(current_post)'''
        return redirect('/')


class note(View):
    def get(self, request, post_id):  # Обрабтчик клика на кнопку "Уже прочитано"
        current_post = BlogPost.objects.get(pk=post_id)
        reader_info = PersonalBlog.objects.get(author=request.user)
        reader_info.noted.add(current_post)  # Этой строкой мы сохраняем номер в БД. Альтернатива - хранение в сессии - закомментирована
        '''manager = FeedManager(request)
        manager.add(current_post)'''  # здесь. Внимание: номера комментируются без учета авторизованного пользователя.
        return redirect('/')


class exit(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class enter(View):
    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        error = ''
        if user is not None:
            login(request, user)
            result = redirect('/')
        else:
            error = 'Неправильный логин или пароль'
            form = AuthForm()
            result = render(request, 'login.html', {'form': form, 'error': error})
        return result
