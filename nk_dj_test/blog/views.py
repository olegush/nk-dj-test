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
    paginate_by = 5


from django.shortcuts import get_object_or_404

class PostListbyAuthorView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name ='blog/post_list_by_author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author=get_object_or_404(BlogAuthor, pk = id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        context = super(PostListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(BlogAuthor, pk = self.kwargs['pk'])
        return context


class PostDetailView(generic.DetailView):
    model = Post


class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 5
