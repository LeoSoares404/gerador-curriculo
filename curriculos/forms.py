from datetime import date

from django import forms
from django.forms import inlineformset_factory

from .models import (
    Curriculo, Experiencia, Formacao, Habilidade, Idioma, Curso, Projeto,
)


def campo_data():
    # format ISO é necessário para o <input type="date"> mostrar o valor salvo
    return forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')


class BootstrapMixin:
    """Adiciona as classes do Bootstrap 5 em todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                classe = 'form-check-input'
            elif isinstance(widget, forms.Select):
                classe = 'form-select'
            else:
                classe = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {classe}".strip()


# ---------- Formulário principal ----------

class CurriculoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Curriculo
        fields = [
            'titulo', 'modelo',
            'nome', 'email', 'telefone', 'cidade', 'data_nascimento',
            'linkedin', 'site', 'resumo',
        ]
        widgets = {
            'modelo': forms.RadioSelect,
            'data_nascimento': campo_data(),
            'resumo': forms.Textarea(attrs={'rows': 4}),
        }


# ---------- Formulários das seções ----------

class ExperienciaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['empresa', 'cargo', 'inicio', 'fim', 'atual', 'descricao']
        widgets = {
            'inicio': campo_data(),
            'fim': campo_data(),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        dados = super().clean()
        inicio, fim, atual = dados.get('inicio'), dados.get('fim'), dados.get('atual')
        if atual and fim:
            self.add_error('fim', 'Deixe a data de fim vazia se este é o trabalho atual.')
        elif fim and inicio and fim < inicio:
            self.add_error('fim', 'A data de fim não pode ser anterior à de início.')
        return dados


class FormacaoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Formacao
        fields = ['instituicao', 'curso', 'nivel', 'inicio', 'fim']
        widgets = {'inicio': campo_data(), 'fim': campo_data()}

    def clean(self):
        dados = super().clean()
        inicio, fim = dados.get('inicio'), dados.get('fim')
        if fim and inicio and fim < inicio:
            self.add_error('fim', 'A data de fim não pode ser anterior à de início.')
        return dados


class HabilidadeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Habilidade
        fields = ['nome', 'nivel']


class IdiomaForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ['idioma', 'nivel']


class CursoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'instituicao', 'ano', 'carga_horaria']

    def clean_ano(self):
        ano = self.cleaned_data['ano']
        if not 1950 <= ano <= date.today().year + 1:
            raise forms.ValidationError('Informe um ano válido.')
        return ano


class ProjetoForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao', 'link']
        widgets = {'descricao': forms.Textarea(attrs={'rows': 3})}


# ---------- Formsets ----------

def _formset(model, form):
    return inlineformset_factory(
        Curriculo, model, form=form, extra=0, can_delete=True,
    )

ExperienciaFormSet = _formset(Experiencia, ExperienciaForm)
FormacaoFormSet = _formset(Formacao, FormacaoForm)
HabilidadeFormSet = _formset(Habilidade, HabilidadeForm)
IdiomaFormSet = _formset(Idioma, IdiomaForm)
CursoFormSet = _formset(Curso, CursoForm)
ProjetoFormSet = _formset(Projeto, ProjetoForm)

# chave = related_name (também é o prefixo padrão de cada formset)
FORMSETS = {
    'experiencias': ExperienciaFormSet,
    'formacoes': FormacaoFormSet,
    'habilidades': HabilidadeFormSet,
    'idiomas': IdiomaFormSet,
    'cursos': CursoFormSet,
    'projetos': ProjetoFormSet,
}