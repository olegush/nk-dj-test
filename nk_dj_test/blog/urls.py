from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('subscribes/', views.SubscribesListView.as_view(), name='subscribes'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/markasread/', views.PostMarkAsRead.as_view(), name='post-mark-as-read'),
    path('author/<int:pk>', views.PostListbyAuthorView.as_view(), name='posts-by-author'),
    path('author/<int:pk>/subscribe/', views.AuthorSubscribe.as_view(), name='subscribe-to-author'),
    path('author/<int:pk>/unsubscribe/', views.AuthorUnsubscribe.as_view(), name='unsubscribe-from-author'),
    path('author/postcreate/', views.PostCreate.as_view(), name='posts-create'),
    path('authors/', views.AuthorsListView.as_view(), name='authors'),
]
