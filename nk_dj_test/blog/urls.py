from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('subscribes/', views.SubscribesListView.as_view(), name='subscribes'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('blogger/<int:pk>', views.PostListbyAuthorView.as_view(), name='posts-by-author'),
    path('blogger/<int:pk>/subscribe/', views.BlogAuthorSubscribe.as_view(), name='subscribe-to-author'),
    path('blogger/<int:pk>/unsubscribe/', views.BlogAuthorUnsubscribe.as_view(), name='unsubscribe-to-author'),
    path('blogger/postcreate/', views.PostCreate.as_view(), name='posts-create'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
]
