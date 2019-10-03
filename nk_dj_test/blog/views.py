from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import View, CreateView, UpdateView
from django.urls import reverse

from .models import Post, BlogAuthor, Status


def index(request):
    return render(
        request,
        'index.html',
    )

class PostListView(generic.ListView):
    model = Post
    paginate_by = 50


class PostListbyAuthorView(generic.ListView):
    model = Post
    paginate_by = 50
    template_name ='blog/post_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk = id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        id = self.request.user.id
        context = super(PostListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        context['logged_used'] = get_object_or_404(BlogAuthor, user = id)
        return context


class SubscribesListView(generic.ListView):
    model = Post
    paginate_by = 50
    template_name ='blog/post_listsubscribes.html'

    def get_queryset(self):
        id = self.request.user.id
        target_author = get_object_or_404(BlogAuthor, user = id)
        return Post.objects.filter(author__in=target_author.subscribed.all())

    def get_context_data(self, **kwargs):
        context = super(SubscribesListView, self).get_context_data(**kwargs)
        return context


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['read'] = Status.objects.filter(user=self.request.user, post=context['post'].id).first()
        return context


class PostMarkAsRead(LoginRequiredMixin, CreateView):
    model = Status
    fields = []

    def get_context_data(self, **kwargs):
        context = super(PostMarkAsRead, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        read_post = Post.objects.select_related('author__user').get(pk=self.kwargs['pk'])
        Status.objects.create(user=self.request.user, post=read_post, read=True)
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'],})


class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 50



class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['name', 'description',]

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        id = self.request.user.pk
        form.instance.author = get_object_or_404(BlogAuthor, user = id)
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk,})


class BlogAuthorSubscribe(LoginRequiredMixin, UpdateView):
    model = BlogAuthor
    fields = []

    def get_success_url(self):
        BlogAuthor.objects.get(user = self.request.user).subscribed.add(self.object)
        return reverse('subscribes')


class BlogAuthorUnsubscribe(LoginRequiredMixin, UpdateView):
    model = BlogAuthor
    fields = []

    def get_success_url(self):
        BlogAuthor.objects.get(user = self.request.user).subscribed.remove(self.object)
        return reverse('subscribes')