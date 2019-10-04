from django.contrib import admin

from django.contrib import admin

from .models import Author, Post

admin.site.register(Author)

@admin.register(Post)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date')
