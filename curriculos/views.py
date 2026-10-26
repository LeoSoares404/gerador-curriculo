from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, 'curriculos/home.html')


@login_required
def painel(request):
    # ponytail: lista simples; o João completa com editar/duplicar/excluir
    return render(request, 'curriculos/painel.html', {
        'curriculos': request.user.curriculos.all(),
    })
