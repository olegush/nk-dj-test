from django.contrib import admin

from django.contrib import admin

from .models import BlogAuthor, Post

admin.site.register(BlogAuthor)

@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
