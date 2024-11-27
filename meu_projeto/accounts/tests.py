from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):

    def test_login_functionality(self):
        # Crie um usuário para testes
        user = User.objects.create_user(username='PamellaMaria', password='MariaSenha123!')
        
        # Tente fazer login com as credenciais do usuário
        response = self.client.post(reverse('login'), {'username': 'PamellaMaria', 'password': 'MariaSenha123!'})
        
        # Verifique se o usuário foi redirecionado para a página de perfil
        self.assertRedirects(response, reverse('profile_list'))  