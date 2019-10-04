from datetime import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    about = models.TextField(max_length=1000)
    subscribed = models.ManyToManyField('self', symmetrical=False, verbose_name="subscribed", related_name="subscribed_to", blank=True)

    def get_absolute_url(self):
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        return self.user.username


class Post(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=3000)
    post_date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user = Author.objects.get(id = self.author_id)
        subject = f'New post added by {user}'
        message = f'{user} just added <a href="/blog/post/{self.id}/">new post</a>'
        recipient_list = [author.user.email  for author in Author.objects.all() if user in author.subscribed.all()]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list )

    def __str__(self):
        return self.name


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'user: {self.user}, post: {self.post}'
