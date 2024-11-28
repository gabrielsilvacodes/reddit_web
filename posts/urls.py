from django.urls import path
from .views import (
    PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView
)
from .views import (
    CommunityListView, CommunityCreateView, CommunityUpdateView, CommunityDeleteView, CommunityDetailView
)
from .views import CommentCreateView, CommentDeleteView
from .views import VoteCreateView, VoteDeleteView
from django.contrib import admin
from django.urls import path, include  # Importa include para incluir as URLs do app



urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('communities/', CommunityListView.as_view(), name='community_list'),
    path('communities/create/', CommunityCreateView.as_view(), name='community_create'),
    path('communities/<int:pk>/update/', CommunityUpdateView.as_view(), name='community_update'),
    path('communities/<int:pk>/delete/', CommunityDeleteView.as_view(), name='community_delete'),
    path('communities/<int:pk>/', CommunityDetailView.as_view(), name='community_detail'),
    path('comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('votes/create/', VoteCreateView.as_view(), name='vote_create'),
    path('votes/<int:pk>/delete/', VoteDeleteView.as_view(), name='vote_delete'),
    path('admin/', admin.site.urls),
    
    

   

]





