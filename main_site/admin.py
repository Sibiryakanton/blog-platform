from django.contrib import admin
from .models import *
from .forms import *
admin.site.register(PersonalBlog)
# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    
    list_display = ('date_published','author','title', 'already_sent')
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['-date_published']
    search_field = ['title']
    exclude=()
	
admin.site.register(BlogPost, BlogPostAdmin)