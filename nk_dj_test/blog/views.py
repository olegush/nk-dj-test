from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.db.models import F, Q, Case, When


from .models import Post, Author, Status


def index(request):
    return render(
        request,
        'index.html'
    )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.all()
        status_case = Case(When(status__user=user, then='status__read'))
        return posts.annotate(status__read=status_case)


class PostListbyAuthorView(generic.ListView):
    model = Post
    paginate_by = 50
    template_name = 'blog/post_list_by_author.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['author'] = Author.objects.get(pk=self.kwargs['pk'])
        context['logged_used'] = Author.objects.get(user=user_id)
        return context

    def get_queryset(self):
        author = Author.objects.get(pk=self.kwargs['pk'])
        posts = Post.objects.filter(author=author)
        return posts.annotate(status__read=F('status__read'))


class SubscribesListView(generic.ListView):
    model = Post
    paginate_by = 50
    template_name = 'blog/post_listsubscribes.html'

    def get_queryset(self):
        author = Author.objects.get(user=self.request.user.id)
        posts = Post.objects.filter(author__in=author.subscribed.all())
        return posts.annotate(status__read=F('status__read'))


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post_id = context['post'].id
        context['read'] = Status.objects.filter(user=user, post=post_id).first()
        return context


class PostMarkAsRead(LoginRequiredMixin, CreateView):
    model = Status
    fields = []

    def get_success_url(self):
        post_id = self.kwargs['pk']
        user = self.request.user
        read_post = Post.objects.select_related('author__user').get(pk=post_id)
        Status.objects.create(user=user, post=read_post, read=True)
        return reverse('post-detail', kwargs={'pk': post_id})


class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 50


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['name', 'description']

    def form_valid(self, form):
        id = self.request.user.pk
        form.instance.author = Author.objects.get(user=id)
        return super().form_valid(form)

    def get_success_url(self):
        post_id = self.object.pk
        return reverse('post-detail', kwargs={'pk': post_id})


class AuthorSubscribe(LoginRequiredMixin, UpdateView):
    model = Author
    fields = []

    def get_success_url(self):
        user = self.request.user
        Author.objects.get(user=user).subscribed.add(self.object)
        return reverse('subscribes')


class AuthorUnsubscribe(LoginRequiredMixin, UpdateView):
    model = Author
    fields = []

    def get_success_url(self):
        user = self.request.user
        Author.objects.get(user=user).subscribed.remove(self.object)
        return reverse('subscribes')
