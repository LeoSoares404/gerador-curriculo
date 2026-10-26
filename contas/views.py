from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CadastroForm


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        messages.success(request, 'Conta criada! Bem-vindo(a).')
        return redirect('painel')
    return render(request, 'registration/cadastro.html', {'form': form})
