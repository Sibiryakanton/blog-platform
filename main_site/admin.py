from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import *
admin.site.register(PersonalBlog)
# Register your models here.


class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm

    list_display = ('date_published', 'author', 'title', 'already_sent')
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['-date_published']
    search_field = ['title']
    exclude = ()

    def save_model(self, request, obj, form, change):
 
        current_blog = PersonalBlog.objects.get(author=obj.author)
        obj.save()
        current_blog.posts.add(BlogPost.objects.get(pk=obj.pk))
        obj.save()

        if obj.order_to_sent:
            mail_host = "oriflamesender@gmail.com"
            user_list = User.objects.all()
            recipients = []
            for user in user_list:
                if user.email == '' or user.email == obj.author.email:
                    continue
                else:
                    recipients.append(user.email)
            message = 'У пользователя {0} в блоге появилась новая запись!Ссылка:{1}'.format(obj.author, 'http://' + request.get_host() + obj.get_absolute_url())
            subject = 'Новый пост'
            send_mail(subject, message, mail_host, recipients, fail_silently=False)
            obj.order_to_sent = False  # Двойная проверка нужна на случай,если пользователь захочет оповестить несколько раз
            obj.already_sent = True
            obj.save()

admin.site.register(BlogPost, BlogPostAdmin)
