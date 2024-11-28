from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Community, Comment, Vote

# Página inicial
def home(request):
    posts_with_votes = Post.objects.select_related('community', 'author').annotate(
        total_votes=Sum('vote__value'),
        total_comments=Count('comments'),
    ).order_by('-pub_date')

    if request.user.is_authenticated:
        posts_with_votes = posts_with_votes.annotate(
            user_vote=Case(
                When(vote__user=request.user, then='vote__value'),
                default=0,
                output_field=IntegerField(),
            )
        )

    communities = Community.objects.annotate(member_count=Count('members')).order_by('-member_count')[:5]
    communities_with_rank = [(index + 1, community) for index, community in enumerate(communities)]

    return render(request, 'home.html', {
        'posts': posts_with_votes,
        'communities_with_rank': communities_with_rank,
    })

# Página para visualizar todas as comunidades e criar uma nova
@login_required
def view_all(request):
    communities = Community.objects.annotate(member_count=Count('members')).order_by('-member_count')
    return render(request, 'view_all.html', {'communities': communities})


# Página específica de uma comunidade
@login_required
def aba_comunidade(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.annotate(total_votes=Sum('vote__value')).order_by('-pub_date')
    is_creator = request.user == community.creator

    return render(request, 'aba_comunidade.html', {
        'community': community,
        'posts': posts,
        'is_creator': is_creator,
    })

# Criar ou editar comunidade (genérico)
@login_required
def community_form(request, community_id=None):
    # Obtemos a comunidade se o ID for fornecido e o usuário for o criador
    community = get_object_or_404(Community, id=community_id, creator=request.user) if community_id else None

    if request.method == 'POST':
        # Coleta os dados do formulário
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validação básica
        if name and description:
            if community:
                # Atualiza a comunidade existente
                community.name = name
                community.description = description
                community.save()
            else:
                # Cria uma nova comunidade
                Community.objects.create(
                    name=name,
                    description=description,
                    creator=request.user
                )
            return redirect('view_all')  # Redireciona após salvar

    # Dados iniciais para edição ou criação
    initial_data = {
        'name': community.name if community else '',
        'description': community.description if community else ''
    }

    return render(request, 'community_form.html', {
        'community': community,
        'initial_data': initial_data,  # Passa os valores iniciais para o template
    })

# Deletar comunidade
@login_required
def delete_community(request, community_id):
    community = get_object_or_404(Community, id=community_id, creator=request.user)
    if request.method == 'POST':
        community.delete()
        return redirect('view_all')
    return render(request, 'delete_community.html', {'community': community})

# CRUD para Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'community']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['communities'] = Community.objects.all()  # Adiciona todas as comunidades ao contexto
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'community']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# Votação em Posts
@login_required
def create_vote(request, post_id, value):
    post = get_object_or_404(Post, id=post_id)
    vote, created = Vote.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'value': value}
    )

    if not created and vote.value == value:
        vote.delete()
        value = 0

    total_votes = Vote.objects.filter(post=post).aggregate(Sum('value'))['value__sum'] or 0

    return JsonResponse({
        'total_votes': total_votes,
        'current_vote': value,
    })

# Busca
def search(request):
    query = request.GET.get('q', '')
    communities = Community.objects.filter(name__icontains=query) if query else Community.objects.none()
    posts = Post.objects.filter(title__icontains=query) if query else Post.objects.none()

    return render(request, 'search_results.html', {
        'query': query,
        'communities': communities,
        'posts': posts,
    })

# Detalhes do post e comentários
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('pub_date')

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content', '').strip()
            if content:
                parent_id = request.POST.get('parent', None)
                parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None
                Comment.objects.create(
                    content=content,
                    post=post,
                    author=request.user,
                    parent=parent_comment
                )
                return redirect('post_detail', pk=post.pk)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

# Apagar comentário
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_superuser:
        comment.delete()
        return redirect('post_detail', pk=comment.post.id)
    return JsonResponse({'error': 'Você não tem permissão para deletar este comentário'}, status=403)

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user in community.members.all():
        community.members.remove(request.user)
    return redirect('view_all')

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.members.all():
        community.members.add(request.user)
    return redirect('view_all')
