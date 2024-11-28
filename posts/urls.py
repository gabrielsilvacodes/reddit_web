from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Página de listagem de todas as comunidades
    path('communities/', views.view_all, name='view_all'),

    # Página específica de uma comunidade
    path('communities/<int:community_id>/', views.aba_comunidade, name='aba_comunidade'),

    # Criar nova comunidade
    path('communities/new/', views.community_form, name='community_create'),

    path('communities/<int:community_id>/edit/', views.community_form, name='edit_community'),

    # Deletar comunidade
    path('communities/<int:community_id>/delete/', views.delete_community, name='delete_community'),

    # CRUD para Post
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # Criar novo post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),  # Editar post existente
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),  # Deletar post existente

    # Votação em Posts
    path('post/<int:post_id>/vote/up/', views.create_vote, {'value': 1}, name='post_upvote'),  # Upvote em post
    path('post/<int:post_id>/vote/down/', views.create_vote, {'value': -1}, name='post_downvote'),  # Downvote em post

    # Busca
    path('search/', views.search, name='search'),

    # Detalhes do Post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Gerenciamento de comunidades (entrar/sair)
    path('communities/<int:community_id>/join/', views.join_community, name='join_community'),  # Entrar na comunidade
    path('communities/<int:community_id>/leave/', views.leave_community, name='leave_community'),  # Sair da comunidade

    # Deletar comentário
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
