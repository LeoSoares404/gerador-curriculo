from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from .exemplo import contexto_exemplo
from .models import Curriculo


def home(request):
    return render(request, 'curriculos/home.html')


@login_required
def painel(request):
    # ponytail: lista simples; o João completa com editar/duplicar/excluir
    return render(request, 'curriculos/painel.html', {
        'curriculos': request.user.curriculos.all(),
    })


def exemplo(request, modelo):
    """Mostra um modelo preenchido com dados fictícios (testes e miniaturas)."""
    if modelo not in dict(Curriculo.MODELOS):
        raise Http404
    return render(request, f'curriculos/modelos/{modelo}.html', contexto_exemplo(modelo))
