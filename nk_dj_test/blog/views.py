from django.shortcuts import render
from django.views import generic
from .models import Post, BlogAuthor
from django.contrib.auth.models import User


def index(request):
    return render(
        request,
        'index.html',
    )

class PostListView(generic.ListView):
    model = Post
    paginate_by = 50


from django.shortcuts import get_object_or_404


class PostListbyAuthorView(generic.ListView):
    model = Post
    paginate_by = 50
    template_name ='blog/post_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        print(id)
        target_author=get_object_or_404(BlogAuthor, pk = id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        id = self.request.user.id
        context = super(PostListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
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


class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


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
