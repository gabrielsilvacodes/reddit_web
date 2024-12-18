from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    """Modelo que representa uma comunidade."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    description = models.TextField(verbose_name="Descrição")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Criador")
    members = models.ManyToManyField(
        User, related_name='communities', blank=True, verbose_name="Membros"
    )

    def __str__(self):
        return self.name

    @property
    def members_count(self):
        """Retorna o número de membros da comunidade."""
        return self.members.count()

    class Meta:
        verbose_name = "Comunidade"
        verbose_name_plural = "Comunidades"


class Post(models.Model):
    """Modelo que representa uma postagem dentro de uma comunidade."""
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(verbose_name="Conteúdo")
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name='posts', verbose_name="Comunidade"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")
    image = models.ImageField(
        upload_to='posts/images/%Y/%m/%d/', blank=True, null=True, verbose_name="Imagem"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"


class Comment(models.Model):
    """Modelo que representa comentários feitos em postagens."""
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='comments', verbose_name="Postagem"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Conteúdo")
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="Resposta"
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Publicação")

    def __str__(self):
        return self.content[:50]

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"


class Vote(models.Model):
    """Modelo que representa votos (upvote/downvote) em posts ou comentários."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Postagem"
    )
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Comentário"
    )
    value = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')], verbose_name="Valor")

    class Meta:
        unique_together = ('user', 'post', 'comment')
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        if self.post:
            return f"{self.user.username} votou {self.value} no post '{self.post.title}'"
        return f"{self.user.username} votou {self.value} no comentário '{self.comment.content[:50]}'"
