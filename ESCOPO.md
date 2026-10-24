# Gerador de Currículo — Escopo do Projeto

Trabalho da faculdade: site onde o usuário preenche seus dados e gera um currículo pronto para baixar/imprimir.

## Stack
- **Back-end:** Python + Django (SQLite em desenvolvimento)
- **Front-end:** HTML, CSS, JavaScript, Bootstrap 5 (templates do Django)

## Objetivo
Permitir que qualquer pessoa crie, edite e exporte um currículo profissional de forma simples, escolhendo entre alguns modelos visuais.

## Funcionalidades

### 1. Contas de usuário
- Cadastro, login e logout (sistema de autenticação nativo do Django)
- Recuperação de senha (opcional)
- Cada usuário vê e edita apenas os próprios currículos

### 2. Currículos (CRUD)
- Criar, listar, editar, duplicar e excluir currículos
- Um usuário pode ter vários currículos (ex.: um por área/vaga)

### 3. Seções do currículo
- **Dados pessoais:** nome, e-mail, telefone, cidade/estado, LinkedIn, GitHub/portfólio, foto (opcional)
- **Resumo / objetivo profissional**
- **Experiência profissional:** empresa, cargo, data início/fim (ou "atual"), descrição
- **Formação acadêmica:** instituição, curso, nível, data início/fim
- **Habilidades:** nome e nível (básico / intermediário / avançado)
- **Idiomas:** idioma e nível
- **Cursos e certificações:** nome, instituição, ano
- **Projetos (opcional):** nome, descrição, link

Seções com vários itens (experiência, formação etc.) permitem adicionar/remover itens dinamicamente no formulário (JS + formsets do Django).

### 4. Modelos (templates) de currículo
- 5 layouts: Clássico, Moderno, Minimalista, Criativo e Executivo
- Todos usam os mesmos dados; trocar de modelo não perde nada
- Pré-visualização antes de exportar

### 5. Exportação
- Página de impressão otimizada (CSS `@media print`) → "Salvar como PDF" pelo navegador
- Exportação direta em PDF no servidor (opcional, ex.: xhtml2pdf / WeasyPrint)

### 6. Gerar currículo a partir de texto livre (opcional — IA)
- O usuário escreve um texto sobre si (ex.: "Sou Ana, formada em ADS em 2023, trabalhei 2 anos como suporte...")
- O site envia o texto para uma API de IA (ex.: API do Claude), que devolve os dados em JSON separados por seção
- O editor é **preenchido** com o resultado; o usuário revisa, corrige e só então salva
- É um atalho: o preenchimento manual continua funcionando sem IA

## Páginas
| Página | Descrição |
|---|---|
| Home | Apresentação do site e botão "Criar meu currículo" |
| Cadastro / Login | Autenticação |
| Painel (Meus currículos) | Lista dos currículos do usuário |
| Editor | Formulário por seções para preencher o currículo, incluindo a escolha do modelo |
| Gerar por texto | Caixa de texto livre que pré-preenche o editor (opcional, IA) |
| Visualização | Currículo renderizado, pronto para imprimir/baixar |

## Modelo de dados (Django)
- `User` (nativo do Django)
- `Curriculo` — usuário (FK), título, modelo escolhido, nome, e-mail, telefone, cidade, linkedin, site, foto, resumo, criado_em, atualizado_em
- `Experiencia` — curriculo (FK), empresa, cargo, inicio, fim, atual, descricao
- `Formacao` — curriculo (FK), instituicao, curso, nivel, inicio, fim
- `Habilidade` — curriculo (FK), nome, nivel
- `Idioma` — curriculo (FK), idioma, nivel
- `Curso` — curriculo (FK), nome, instituicao, ano
- `Projeto` — curriculo (FK), nome, descricao, link

## Estrutura de pastas prevista
```
gerador-curriculo/
├── manage.py
├── requirements.txt
├── config/            # settings, urls do projeto
├── contas/            # cadastro, login, logout
├── curriculos/        # currículos (models, views, forms, urls, templates)
├── templates/         # base.html
└── static/            # css, js, img
```

## Requisitos não funcionais
- Layout responsivo (Bootstrap)
- Validação de formulários no front (HTML5/JS) e no back (Django forms)
- Proteção CSRF e acesso restrito aos dados do próprio usuário
- Painel admin do Django para gerenciar dados

## Etapas de desenvolvimento
1. Configurar projeto Django, apps e Bootstrap
2. Autenticação (cadastro/login/logout)
3. Models + migrations + admin
4. CRUD de currículos e formulários das seções
5. Templates de visualização (layouts)
6. Impressão / exportação PDF
7. Ajustes visuais, testes e apresentação
8. (Opcional) Geração do currículo a partir de texto com IA

## Equipe e divisão de tarefas
| Integrante | Área | Principais entregas | Diário |
|---|---|---|---|
| Leonardo Soares | Base, contas e integração | setup do projeto, `base.html`, app `contas`, segurança, testes, IA (opcional) | [diário](diarios/leonardo-soares.md) |
| João Lucas | Dados e editor | models, admin, forms/formsets, editor + `editor.js`, painel, duplicar/excluir | [diário](diarios/joao-lucas.md) |
| Renan Nantes | Visual, modelos e exportação | home, `style.css`, os 5 modelos, visualização, impressão/PDF | [diário](diarios/renan-nantes.md) |

**Dependências entre as partes:**
- Leonardo faz a etapa 1 primeiro (projeto criado e `base.html`), porque os outros dois trabalham em cima dela.
- Enquanto os models do João não ficam prontos, o Renan pode montar os 5 modelos em HTML estático com dados de exemplo e depois trocar pelas variáveis do Django.
- Cada pessoa mexe principalmente nos próprios arquivos, o que evita conflito no Git.

Cada integrante registra no próprio diário o que fez, as decisões tomadas e os problemas encontrados.

## Fora do escopo (por enquanto)
- Pagamentos, planos premium
- Integração com LinkedIn
