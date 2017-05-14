from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.urls import reverse
from django.core.mail import send_mail
class BlogPost(models.Model):
	class Meta:
		verbose_name='Пост пользователя'
		verbose_name_plural='Посты пользователей'
		
	author = models.ForeignKey(User)
	title = models.CharField('Заголовок', max_length=50)
	text = models.TextField()
	date_published=models.DateTimeField()
	order_to_sent = models.BooleanField('Разослать уведомления?', default=False)
	already_sent = models.BooleanField('Уведомления разосланы', default=False)
	def __str__(self):
		return self.title
	
	@models.permalink
	def get_absolute_url(self):
		return ('post_page', (), {'username': self.author.username,'post_pk': self.pk,})
	

	def test_url(self):
		return reverse('post_page', args=[self.author.username, self.pk])
		
	def save(self,*args, **kwargs ):
	
		current_blog = PersonalBlog.objects.get(author=self.author)
		super(BlogPost, self).save(*args, **kwargs)
		current_blog.posts.add(BlogPost.objects.get(pk=self.pk))
		super(BlogPost, self).save(*args, **kwargs)
		if self.order_to_sent==True:
			mail_host = "oriflamesender@gmail.com" 
			user_list = User.objects.all()
			recipients= []
			for user in user_list:
				if user.email=='' or user.email==self.author.email:
					continue
				else:
					recipients.append(user.email)
			message = '''
				У пользователя {0} в блоге появилась новая запись!Ссылка:
				{1}'''.format(self.author, self.test_url()) #self.get_absolute_url()
			subject= 'Новый пост'
			send_mail(subject, message, mail_host, recipients, fail_silently=False)
			self.order_to_sent=False #Двойная проверка нужна на случай,если пользователь захочет оповестить несколько раз
			self.already_sent=True
			super(BlogPost, self).save(*args, **kwargs)
		
class PersonalBlog(models.Model): #Модель хранения данных о публикациях, подписках и подписчиках
	class Meta:
		verbose_name='Блог пользователя'
		verbose_name_plural='Блоги пользователей'
		
	author = models.ForeignKey(User, related_name='author')
	posts = models.ManyToManyField(BlogPost, verbose_name='Посты', blank=True, related_name='posts')
	feeds = models.ManyToManyField(User, verbose_name='Подписки', blank=True, related_name='feeds')
	followers = models.ManyToManyField(User, verbose_name='Подписчики', blank=True, related_name='followers')
	noted=models.ManyToManyField(BlogPost, blank=True, verbose_name='Прочитано', related_name='noted')
	def __str__(self):
		return self.author.username