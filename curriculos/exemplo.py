"""Currículo de exemplo (não salvo no banco) para testar e pré-visualizar os modelos."""
from datetime import date

from .models import Curriculo, Curso, Experiencia, Formacao, Habilidade, Idioma, Projeto


def contexto_exemplo(modelo):
    return {
        'curriculo': Curriculo(
            titulo='Exemplo', modelo=modelo,
            nome='Ana Beatriz Souza', email='ana.souza@email.com', telefone='(11) 91234-5678',
            cidade='São Paulo/SP', data_nascimento=date(2001, 5, 14),
            linkedin='https://linkedin.com/in/anasouza', site='https://github.com/anasouza',
            resumo='Desenvolvedora júnior com experiência em suporte técnico e projetos web em Python '
                   'e Django. Busco uma oportunidade para crescer na área de desenvolvimento back-end.',
        ),
        'experiencias': [
            Experiencia(empresa='Tech Soluções', cargo='Desenvolvedora Júnior', inicio=date(2024, 3, 1),
                        atual=True, descricao='Manutenção de sistemas internos em Django e criação de APIs.'),
            Experiencia(empresa='Empresa X', cargo='Analista de Suporte', inicio=date(2022, 1, 10),
                        fim=date(2024, 2, 28), descricao='Atendimento a usuários e manutenção de computadores.'),
        ],
        'formacoes': [
            Formacao(instituicao='Fatec São Paulo', curso='Análise e Desenvolvimento de Sistemas',
                     nivel='graduacao', inicio=date(2021, 2, 1), fim=date(2023, 12, 15)),
        ],
        'habilidades': [
            Habilidade(nome='Python', nivel='avancado'),
            Habilidade(nome='Django', nivel='intermediario'),
            Habilidade(nome='HTML/CSS', nivel='intermediario'),
            Habilidade(nome='SQL', nivel='basico'),
        ],
        'idiomas': [
            Idioma(idioma='Português', nivel='nativo'),
            Idioma(idioma='Inglês', nivel='intermediario'),
        ],
        'cursos': [
            Curso(nome='Python para Web', instituicao='Alura', ano=2023, carga_horaria=40),
        ],
        'projetos': [
            Projeto(nome='Gerador de Currículo', descricao='Site em Django para criar currículos.',
                    link='https://github.com/anasouza/gerador'),
        ],
    }
