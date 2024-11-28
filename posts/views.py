from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Post, Community, Comment, Vote


# List
class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

# Create
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'community']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

# Update
class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_list')

# Delete
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# Detail
class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


# List
class CommunityListView(ListView):
    model = Community
    template_name = 'posts/community_list.html'
    context_object_name = 'communities'

# Create
class CommunityCreateView(CreateView):
    model = Community
    fields = ['name', 'description']
    template_name = 'posts/community_form.html'
    success_url = reverse_lazy('community_list')

# Update
class CommunityUpdateView(UpdateView):
    model = Community
    fields = ['name', 'description']
    template_name = 'posts/community_form.html'
    success_url = reverse_lazy('community_list')

# Delete
class CommunityDeleteView(DeleteView):
    model = Community
    template_name = 'posts/community_confirm_delete.html'
    success_url = reverse_lazy('community_list')

# Detail
class CommunityDetailView(DetailView):
    model = Community
    template_name = 'posts/community_detail.html'


# Create
class CommentCreateView(CreateView):
    model = Comment
    fields = ['content', 'post', 'author', 'parent']
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('post_list')

# Delete
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# Create
class VoteCreateView(CreateView):
    model = Vote
    fields = ['user', 'post', 'comment', 'value']
    template_name = 'posts/vote_form.html'
    success_url = reverse_lazy('post_list')

# Delete
class VoteDeleteView(DeleteView):
    model = Vote
    template_name = 'posts/vote_confirm_delete.html'
    success_url = reverse_lazy('post_list')

def index(request):
    return render(request, 'home.html') #renderiza o aquivo html

def view_all(request):
    return render(request, 'view_all.html')

def aba_comunidade(request):
    return render(request, 'aba_comunidade.html')

