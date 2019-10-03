from django.db import models

from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class BlogAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    about = models.TextField(max_length=1000)
    subscribed = models.ManyToManyField('self', symmetrical=False, verbose_name="subscribed", related_name="subscribed_to", blank=True)

    def get_absolute_url(self):
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Post(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(BlogAuthor, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=3000)
    post_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'user: {self.user}, post: {self.post}'
