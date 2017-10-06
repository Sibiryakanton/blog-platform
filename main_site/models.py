from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.urls import reverse
from django.core.mail import send_mail


class BlogPost(models.Model):
    class Meta:
        verbose_name = 'Пост пользователя'
        verbose_name_plural = 'Посты пользователей'

    author = models.ForeignKey(User)
    title = models.CharField('Заголовок', max_length=50)
    text = models.TextField()
    date_published = models.DateTimeField()
    order_to_sent = models.BooleanField('Разослать уведомления?', default=False)
    already_sent = models.BooleanField('Уведомления разосланы', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('post_page', args=[self.author.username, self.pk])
        return url


class PersonalBlog(models.Model):  # Модель хранения данных о публикациях, подписках и подписчиках
    class Meta:
        verbose_name = 'Блог пользователя'
        verbose_name_plural = 'Блоги пользователей'

    author = models.ForeignKey(User, related_name='author')
    posts = models.ManyToManyField(BlogPost, verbose_name='Посты', blank=True, related_name='posts')
    feeds = models.ManyToManyField(User, verbose_name='Подписки', blank=True, related_name='feeds')
    followers = models.ManyToManyField(User, verbose_name='Подписчики', blank=True, related_name='followers')
    noted = models.ManyToManyField(BlogPost, blank=True, verbose_name='Прочитано', related_name='noted')

    def __str__(self):
        return self.author.username
