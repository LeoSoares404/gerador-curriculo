from django.contrib import admin
from .models import Curriculo, Experiencia, Formacao, Habilidade, Idioma, Curso, Projeto


class ExperienciaInline(admin.StackedInline):
    model = Experiencia
    extra = 0


class FormacaoInline(admin.StackedInline):
    model = Formacao
    extra = 0


class HabilidadeInline(admin.TabularInline):
    model = Habilidade
    extra = 0


class IdiomaInline(admin.TabularInline):
    model = Idioma
    extra = 0


class CursoInline(admin.TabularInline):
    model = Curso
    extra = 0
    fields = ('nome', 'instituicao', 'ano', 'carga_horaria')


class ProjetoInline(admin.StackedInline):
    model = Projeto
    extra = 0


@admin.register(Curriculo)
class CurriculoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'nome', 'idade', 'modelo', 'atualizado_em')
    list_filter = ('modelo',)
    search_fields = ('titulo', 'nome', 'usuario__username')
    readonly_fields = ('idade', 'criado_em', 'atualizado_em')

    fieldsets = (
        ('Currículo', {
            'fields': ('usuario', 'titulo', 'modelo'),
        }),
        ('Dados pessoais', {
            'fields': ('nome', 'email', 'telefone', 'cidade',
                       'data_nascimento', 'idade'),
        }),
        ('Links', {
            'fields': ('linkedin', 'site'),
        }),
        ('Resumo / objetivo', {
            'fields': ('resumo',),
        }),
        ('Registro', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',),
        }),
    )

    inlines = [ExperienciaInline, FormacaoInline, HabilidadeInline,
               IdiomaInline, CursoInline, ProjetoInline]

    @admin.display(description='Idade')
    def idade(self, obj):
        return obj.idade if obj.idade is not None else '—'
