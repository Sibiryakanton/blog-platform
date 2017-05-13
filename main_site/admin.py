from django.contrib import admin
from .models import *
from .forms import *
admin.site.register(PersonalBlog)
# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    
    list_display = ('author','title', 'slug','date_published', 'already_sent')
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['title']
    search_field = ['title']
    exclude=()
    prepopulated_fields={'slug':('title',)}
	
admin.site.register(BlogPost, BlogPostAdmin)