from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Community, Comment, Vote

# Página inicial
def home(request):
    if request.user.is_authenticated:
        # Caso o usuário esteja autenticado
        posts_with_votes = Post.objects.select_related('community', 'author').annotate(
            total_votes=Sum('vote__value'),
            user_vote=Case(
                When(vote__user=request.user, then=Sum('vote__value')),
                default=0,
                output_field=IntegerField(),
            )
        ).order_by('-pub_date')
    else:
        # Caso o usuário seja anônimo
        posts_with_votes = Post.objects.select_related('community', 'author').annotate(
            total_votes=Sum('vote__value')
        ).order_by('-pub_date')

    communities = Community.objects.annotate(member_count=Count('members')).order_by('-member_count')[:5]
    communities_with_rank = [(index + 1, community) for index, community in enumerate(communities)]

    return render(request, 'home.html', {
        'posts': posts_with_votes,
        'communities_with_rank': communities_with_rank,
    })


# Página para visualizar todas as comunidades
def view_all(request):
    communities = Community.objects.all().order_by('name')
    return render(request, 'view_all.html', {'communities': communities})

# Página específica de uma comunidade
def aba_comunidade(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.annotate(
        total_votes=Sum('vote__value')
    ).order_by('-pub_date')
    return render(request, 'aba_comunidade.html', {'community': community, 'posts': posts})

# CRUD para Post
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'community']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('home')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('home')

# CRUD para Community
class CommunityCreateView(CreateView):
    model = Community
    fields = ['name', 'description']
    template_name = 'posts/community_form.html'
    success_url = reverse_lazy('view_all')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class CommunityUpdateView(UpdateView):
    model = Community
    fields = ['name', 'description']
    template_name = 'posts/community_form.html'
    success_url = reverse_lazy('view_all')

class CommunityDeleteView(DeleteView):
    model = Community
    template_name = 'posts/community_confirm_delete.html'
    success_url = reverse_lazy('view_all')

# CRUD para Comment
class CommentCreateView(CreateView):
    model = Comment
    fields = ['content', 'post', 'parent']
    template_name = 'posts/comment_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Votação em Posts
def create_vote(request, post_id, value):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'value': value}
        )

        if not created and vote.value == value:
            # Remove o voto se o mesmo botão for clicado novamente
            vote.delete()
            value = 0  # Valor atual do voto é zerado

        # Soma total de votos
        total_votes = Vote.objects.filter(post=post).aggregate(Sum('value'))['value__sum'] or 0

        return JsonResponse({
            'total_votes': total_votes,
            'current_vote': value,  # Retorna o voto atual
        })

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Busca
def search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ) if query else Post.objects.none()
    communities = Community.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Community.objects.none()

    return render(request, 'search_results.html', {
        'query': query,
        'posts': posts,
        'communities': communities
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user in community.members.all():
        community.members.remove(request.user)
    return redirect('view_all')

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user in community.members.all():
        community.members.remove(request.user)
    else:
        community.members.add(request.user)
    return redirect('view_all')

# Detalhes de uma comunidade
def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.all().order_by('-pub_date')
    return render(request, 'community_detail.html', {'community': community, 'posts': posts})



from django.shortcuts import render

def post_form(request):
    return render(request, 'post_form.html')

