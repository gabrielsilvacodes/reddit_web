# meu_app/views.py



from django.shortcuts import render

def index(request):
    return render(request, 'home.html')  # Renderiza o template 'home.html'

def view_all(request):
    return render(request, 'view_all.html')

def aba_comunidade(request):
    return render(request, 'aba_comunidade.html')

    
