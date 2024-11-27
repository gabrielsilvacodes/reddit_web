from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Profile

# View para registro de usuário
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Após salvar o usuário, autentique e faça login automaticamente
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('profile_list')  # Redireciona para a lista de perfis após o registro
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'accounts/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 10  # Número de itens por página
    ordering = ['user__username'] 
    login_url = 'login' 