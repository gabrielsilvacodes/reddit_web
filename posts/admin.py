from django.contrib import admin
from .models import Community, Post, Comment, Vote

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')  # Exibe nome e criador da comunidade na lista

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'author', 'pub_date')  # Informações básicas dos posts

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'author', 'pub_date')  # Resumo básico dos comentários

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'value')

    def comment(self, obj):
        return obj.comment.content if obj.comment else 'N/A'

# Registra os modelos com suas configurações simplificadas
admin.site.register(Community, CommunityAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
