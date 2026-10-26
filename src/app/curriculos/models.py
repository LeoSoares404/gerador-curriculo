from django.conf import settings
from django.db import models
from datetime import date


class Curriculo(models.Model):
    MODELOS = [
        ('classico', 'Clássico'),
        ('moderno', 'Moderno'),
        ('minimalista', 'Minimalista'),
        ('criativo', 'Criativo'),
        ('executivo', 'Executivo'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='curriculos'
    )
    data_nascimento = models.DateField('data de nascimento', null=True, blank=True)
    @property
    def idade(self):
        if not self.data_nascimento:
            return None
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
    )
    titulo = models.CharField('título', max_length=100)  # só aparece no painel
    modelo = models.CharField(max_length=20, choices=MODELOS, default='classico')

    # dados pessoais
    nome = models.CharField(max_length=150)
    email = models.EmailField('e-mail')
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField('cidade/estado', max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    site = models.URLField('GitHub/portfólio', blank=True)

    resumo = models.TextField('resumo / objetivo', blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-atualizado_em']

    def __str__(self):
        return f'{self.titulo} ({self.usuario})'


class Experiencia(models.Model):
    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='experiencias'
    )
    empresa = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    inicio = models.DateField('início')
    fim = models.DateField(null=True, blank=True)
    atual = models.BooleanField('trabalho atual', default=False)
    descricao = models.TextField('descrição', blank=True)

    class Meta:
        ordering = ['-inicio']
        verbose_name = 'experiência'
        verbose_name_plural = 'experiências'

    def __str__(self):
        return f'{self.cargo} - {self.empresa}'


class Formacao(models.Model):
    NIVEIS = [
        ('medio', 'Ensino Médio'),
        ('tecnico', 'Técnico'),
        ('graduacao', 'Graduação'),
        ('pos', 'Pós-graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
    ]

    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='formacoes'
    )
    instituicao = models.CharField('instituição', max_length=150)
    curso = models.CharField(max_length=150)
    nivel = models.CharField('nível', max_length=20, choices=NIVEIS)
    inicio = models.DateField('início')
    fim = models.DateField(null=True, blank=True)  # vazio = cursando

    class Meta:
        ordering = ['-inicio']
        verbose_name = 'formação'
        verbose_name_plural = 'formações'

    def __str__(self):
        return f'{self.curso} - {self.instituicao}'


class Habilidade(models.Model):
    NIVEIS = [
        ('basico', 'Básico'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]

    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='habilidades'
    )
    nome = models.CharField(max_length=100)
    nivel = models.CharField('nível', max_length=20, choices=NIVEIS)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nome


class Idioma(models.Model):
    NIVEIS = [
        ('basico', 'Básico'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
        ('fluente', 'Fluente'),
        ('nativo', 'Nativo'),
    ]

    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='idiomas'
    )
    idioma = models.CharField(max_length=60)
    nivel = models.CharField('nível', max_length=20, choices=NIVEIS)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'idiomas'

    def __str__(self):
        return self.idioma


class Curso(models.Model):
    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='cursos'
    )
    nome = models.CharField(max_length=150)
    instituicao = models.CharField('instituição', max_length=150)
    ano = models.PositiveSmallIntegerField()
    carga_horaria = models.PositiveSmallIntegerField('carga horária', null=True, blank=True)

    class Meta:
        ordering = ['-ano']
        verbose_name = 'curso/certificação'
        verbose_name_plural = 'cursos e certificações'

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    curriculo = models.ForeignKey(
        Curriculo, on_delete=models.CASCADE, related_name='projetos'
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField('descrição', blank=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.nome