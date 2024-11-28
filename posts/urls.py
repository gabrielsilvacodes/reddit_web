from django.urls import path
from . import views
from .views import (
    PostCreateView, PostUpdateView, PostDeleteView,
    CommunityCreateView, CommunityUpdateView, CommunityDeleteView,
    CommentCreateView
)

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Página de listagem de todas as comunidades
    path('communities/', views.view_all, name='view_all'),

    # Página específica de uma comunidade
    path('communities/<int:community_id>/', views.aba_comunidade, name='aba_comunidade'),

    # CRUD para Post
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # Criar novo post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),  # Editar post existente
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # Deletar post existente

    # CRUD para Community
    path('community/new/', CommunityCreateView.as_view(), name='community_create'),  # Criar nova comunidade
    path('community/<int:pk>/edit/', CommunityUpdateView.as_view(), name='community_update'),  # Editar comunidade
    path('community/<int:pk>/delete/', CommunityDeleteView.as_view(), name='community_delete'),  # Deletar comunidade

    # Adicionar comentários
    path('comment/new/', CommentCreateView.as_view(), name='comment_create'),  # Criar novo comentário

    # Votos (Upvote e Downvote)
    path('post/<int:post_id>/upvote/', views.create_vote, {'value': 1}, name='post_upvote'),  # Upvote em post
    path('post/<int:post_id>/downvote/', views.create_vote, {'value': -1}, name='post_downvote'),  # Downvote em post

    # Busca
    path('search/', views.search, name='search'),  # Página de busca

    # Entrar e sair da comunidade
    path('community/<int:community_id>/join/', views.join_community, name='join_community'),  # Entrar na comunidade
    path('community/<int:community_id>/leave/', views.leave_community, name='leave_community'),  # Sair da comunidade

    # Detalhes da comunidade
    path('community/<int:community_id>/', views.community_detail, name='community_detail'),  # Página de detalhes da comunidade
]
