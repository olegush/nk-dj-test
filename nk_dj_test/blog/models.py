from django.db import models

from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User


class BlogAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    about = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse('blogs-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=3000)
    post_date = models.DateField(default=date.today)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
